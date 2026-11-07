"""A logical policy model, not an OS sandbox or hardware protection."""
from dataclasses import dataclass, field


@dataclass
class Domain:
    active: set = field(default_factory=lambda: {"A"})
    edges: set = field(default_factory=set)
    stopped: bool = False

    def start(self, name, authorized=False):
        if self.stopped or not authorized or name in self.active:
            return False
        self.active.add(name)
        return True

    def send(self, source, target):
        return (not self.stopped and source in self.active
                and target in self.active and (source, target) in self.edges)

    def stop(self):
        self.stopped = True
        self.active.clear()


def main():
    domain = Domain()
    assert not domain.start("B")
    assert domain.start("B", authorized=True)
    assert not domain.send("A", "B")
    domain.edges.add(("A", "B"))
    assert domain.send("A", "B")
    assert not domain.send("B", "A")
    domain.stop()
    assert not domain.active
    assert not domain.start("C", authorized=True)
    assert not domain.send("A", "B")
    print("PASS policy_model: 8 checks")


if __name__ == "__main__":
    main()
