import dragonfly
import uuid
import collections


class SpeechRecognitionEnvironment:
    def __init__(self, path, rule_builder):
        self.path = path
        self.rule_builder = rule_builder
        self.merged_context = merge_context_iterable(path)

    def load_grammar(self):
        gram = dragonfly.Grammar(name=str(uuid.uuid4()))
        gram.add_rule(self.rule_builder.to_rule())
        gram.set_context(self.merged_context)
        gram.load()
        return gram


def load_environments(map_contexts_to_builder):
    # This approach assumes contexts without a direct ancestor/descendant relationship
    # are mutually exclusive, otherwise multiple overlapping grammars could be active
    # at the same time. Not sure whether that's a problem though.
    # map_contexts_to_builder = {
    #     (contexts.stardew,): stardew.rule_builder(),
    # }
    envs = []
    root = None
    for context_path, rule_builder in map_contexts_to_builder.items():
        env = SpeechRecognitionEnvironment(frozenset(context_path), rule_builder)
        if root is None:
            root = EnvironmentTree(env)
        elif env.path < root.path:
            new_root = EnvironmentTree(env)
            new_root.add_child(root)
            root = new_root
        else:
            root.add_env(env)
        envs.append(env)
    # create contexts that are only active when all descendant contexts are inactive. Postorder
    # traversal so we only need to perform a NOT AND with children rather than all descendants
    for node in root.postorder():
        for child in node.children:
            node.env.merged_context = combine_contexts(
                node.env.merged_context, ~child.env.merged_context
            )
    # env consists of all rules specific to that context as well as all rules in ancestor contexts. Preorder
    # traversal means current node's rules already include all ancestor rules
    for node in root.preorder():
        for child in node.children:
            child.env.rule_builder.merge(node.env.rule_builder)
    return envs


class EnvironmentTree:
    def __init__(self, env):
        self.env = env
        self.children = []

    def add_env(self, env: SpeechRecognitionEnvironment):
        path = env.path
        assert path > self.path
        for child in self.children:
            assert child.path != path
            if child.path < path:
                child.add_env(env)
        self.add_child(EnvironmentTree(env))

    def preorder(self):
        yield self
        for child in self.children:
            yield from child.preorder()

    def postorder(self):
        for child in self.children:
            yield from child.preorder()
        yield self

    @property
    def path(self):
        return self.env.path

    def add_child(self, child):
        new_childen = [child]
        # account for inserting a shorter child than existing children, e.g. vscode into [(), (vscode, python)]
        for old_child in self.children:
            if old_child.path > child.path:
                child.add_child(old_child)
            else:
                new_childen.append(old_child)
        self.children = new_childen


def merge_context_iterable(contexts):
    merged = None
    for ctx in contexts:
        merged = combine_contexts(merged, ctx)
    return merged


def load_grammars(envs):
    for env in envs:
        env.load_grammar()


def combine_contexts(ctx1, ctx2):
    if not ctx1:
        return ctx2
    if not ctx2:
        return ctx1
    return ctx1 & ctx2