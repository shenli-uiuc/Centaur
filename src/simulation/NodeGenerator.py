import random

class NodeGenerator:

    def gen(self, size, nodeNum):
        nodePos = []
        i = 0
        while i < nodeNum:
            x = random.random() * size
            y = random.random() * size

            nodePos.append([x, y])

            i += 1

        return nodePos


def main():
    nodeGenerator = NodeGenerator()
    print nodeGenerator.gen(10, 100)


if __name__ == '__main__':
    main()
