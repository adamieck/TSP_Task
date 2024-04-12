class Graph {
    constructor() {
        this.nodes = new Map();
    }

    addNode(city) {
        this.nodes.set(city, new Map());
    }

    addEdge(city1, city2, time) {
        this.nodes.get(city1).set(city2, time);
        this.nodes.get(city2).set(city1, time);
    }

    getNeighbors(city) {
        return this.nodes.get(city);
    }
}

module.exports = Graph;