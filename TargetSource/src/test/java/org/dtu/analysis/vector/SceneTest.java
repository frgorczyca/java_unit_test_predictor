package org.dtu.analysis.vector;

import org.junit.jupiter.api.Test;

import java.util.Iterator;

import static org.junit.jupiter.api.Assertions.*;

class SceneTest {

    @Test
    void calculateWorldTransform() {
        Scene scene = Scene.createScene2();
        scene.calculateWorldTransform();
        for (Scene.WorldObject item : scene) {
            item.transform.transpose().matmul(item.transform).matmul(item.transformWorld).transpose();
        }
    }

    @Test
    void createScene() {
        Scene.createScene();
    }

    @Test
    void createScene2() {
        Scene.createScene2();
    }
}