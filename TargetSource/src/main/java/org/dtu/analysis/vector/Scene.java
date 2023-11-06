package org.dtu.analysis.vector;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.Random;
import java.util.Stack;

public class Scene implements Iterable<Scene.WorldObject> {

    static int max_depth = 10;
    static int max_length = 10;

    WorldObject root;

    static Random rng = new Random(0);

    @Override
    public Iterator<WorldObject> iterator() {
        return new SceneIterator(this);
    }

    public static class SceneIterator implements Iterator<WorldObject> {

        private Stack<WorldObject> stack1 = new Stack<>();
        private Stack<WorldObject> stack2 = new Stack<>();

        public SceneIterator(Scene scene) {
            stack1.push(scene.root);
        }
        @Override
        public boolean hasNext() {
            return !(stack1.isEmpty() && stack2.isEmpty());
        }

        @Override
        public WorldObject next() {
            if (stack1.isEmpty()) {
                var temp = stack1;
                stack1 = stack2;
                stack2 = temp;
            }
            var obj = stack1.pop();
            for (var child: obj.children) {
                stack2.push(child);
            }
            return obj;

        }
    }


    public static class WorldObject {
        public Mat3x3 transform;

        public Mat3x3 transformWorld;
        public ArrayList<WorldObject> children;

        public WorldObject(Mat3x3 transform) {
            this.transform = transform;
            this.transformWorld = transform;
            this.children = new ArrayList<>();
        }
    }

    public void calculateWorldTransform() {
        calculateWorldTransformRecursive(root, Mat3x3.identity());
    }

    void calculateWorldTransformRecursive(WorldObject object, Mat3x3 parentTransform) {
        object.transformWorld = parentTransform.matmul(object.transform);
        for (int i = 0; i < object.children.size(); i++) {
            calculateWorldTransformRecursive(object.children.get(i), object.transformWorld);
        }
    }

    public static Scene createScene() {
        Scene scene = new Scene();
        Scene.rng = new Random(0);
        scene.root = createWorldObjectRecursive(0);
        return scene;
    }

    public static Scene createScene2() {
        Scene scene = new Scene();
        Scene.rng = new Random(0);
        scene.root = createWorldObjectIterative();
        return scene;
    }

    static WorldObject createWorldObjectRecursive(int depth) {
        var object = new WorldObject(randomMat3x3(rng));
        if (depth != max_depth) {
            var children = rng.nextInt(max_length);
            for (int i = 0; i < children; i++) {
                object.children.add(createWorldObjectRecursive(depth + 1));
            }
        }
        return object;
    }

    static WorldObject createWorldObjectIterative() {
        var root = new WorldObject(randomMat3x3(rng));
        var stack1 = new Stack<WorldObject>();
        var stack2 = new Stack<WorldObject>();
        stack1.push(root);
        var depth = 0;
        while (depth < max_depth) {
            while (!stack1.isEmpty()) {
                var parent = stack1.pop();
                var children = rng.nextInt(max_length);
                for (int j = 0; j < children; j++) {
                    var child = new WorldObject((randomMat3x3(rng)));
                    parent.children.add(child);
                    stack2.push(child);
                }
            }
            var temp = stack1;
            stack1 = stack2;
            stack2 = temp;
            depth++;
        }
        return root;
    }



    static Mat3x3 randomMat3x3(Random rng) {
        return new Mat3x3(
                new Vec3(rng.nextDouble(), rng.nextDouble(), rng.nextDouble()),
                new Vec3(rng.nextDouble(), rng.nextDouble(), rng.nextDouble()),
                new Vec3(rng.nextDouble(), rng.nextDouble(), rng.nextDouble())
        );
    }

}
