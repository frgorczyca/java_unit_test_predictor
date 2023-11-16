package org.dtu.analysis.vector;

public class Mat3x3 {
    public Vec3 r1;
    public Vec3 r2;
    public Vec3 r3;

    public Vec3 c1() {
        return new Vec3(
                r1.x,
                r2.x, // shut up please
                r3.x
        );
    }

    public Vec3 c2() {
        return new Vec3(
                r1.y, // shut up please
                r2.y,
                r3.y
        );
    }

    public Vec3 c3() {
        return new Vec3(
                r1.z,
                r2.z,
                r3.z
        );
    }

    public double a11() {
        return r1.x;
    }
    public double a12() {
        return r1.y;
    }
    public double a13() {
        return r1.z;
    }
    public double a21() {
        return r2.x;
    }
    public double a22() {
        return r2.y;
    }
    public double a23() {
        return r2.z;
    }
    public double a31() {
        return r3.x;
    }
    public double a32() {
        return r3.y;
    }
    public double a33() {
        return r3.z;
    }

    public Mat3x3(Vec3 row1, Vec3 row2, Vec3 row3) {
        this.r1 = row1;
        this.r2 = row2;
        this.r3 = row3;
    }

    public static Mat3x3 zeros() {
        return new Mat3x3(Vec3.zeros(), Vec3.zeros(), Vec3.zeros());
    }

    public static Mat3x3 ones() {
        return new Mat3x3(Vec3.ones(), Vec3.ones(), Vec3.ones());
    }

    public static Mat3x3 identity() {
        return new Mat3x3(
                new Vec3(1, 0, 0),
                new Vec3(0, 1, 0),
                new Vec3(0, 0, 1));
    }

    public Mat3x3 add_c(double rhs) {
        return new Mat3x3(
                this.r1.add_c(rhs),
                this.r2.add_c(rhs),
                this.r3.add_c(rhs)
        );
    }

    public Mat3x3 add_mat(Mat3x3 rhs) {
        return new Mat3x3(
                this.r1.add(rhs.r1),
                this.r2.add(rhs.r2),
                this.r3.add(rhs.r3)
        );
    }

    public Mat3x3 sub_c(double rhs) {
        return new Mat3x3(
                this.r1.sub_c(rhs),
                this.r2.sub_c(rhs),
                this.r3.sub_c(rhs)
        );
    }

    public Mat3x3 sub_mat(Mat3x3 rhs) {
        return new Mat3x3(
                this.r1.sub(rhs.r1),
                this.r2.sub(rhs.r2),
                this.r3.sub(rhs.r3)
        );
    }

    public Mat3x3 mul_c(double rhs) {
        return new Mat3x3(
                this.r1.mul_c(rhs),
                this.r2.mul_c(rhs),
                this.r3.mul_c(rhs)
        );
    }

    /**
     * Elementwise multiply
     */
    public Mat3x3 mul_mat(Mat3x3 rhs) {
        return new Mat3x3(
                this.r1.mul(rhs.r1),
                this.r2.mul(rhs.r2),
                this.r3.mul(rhs.r3)
        );
    }

    public Mat3x3 div_c(double rhs) {
        return new Mat3x3(
                this.r1.div_c(rhs),
                this.r2.div_c(rhs),
                this.r3.div_c(rhs)
        );
    }

    /**
     * Elementwise multiply
     */
    public Mat3x3 div_mat(Mat3x3 rhs) {
        return new Mat3x3(
                this.r1.div(rhs.r1),
                this.r2.div(rhs.r2),
                this.r3.div(rhs.r3)
        );
    }

    public Mat3x3 transpose() {
        return new Mat3x3(
                this.c1(), this.c2(), this.c3()
        );
    }

    public Mat3x3 matmul(Mat3x3 rhs) {
        return new Mat3x3(
                new Vec3(this.r1.dot(rhs.c1()), this.r1.dot(rhs.c2()), this.r1.dot(rhs.c3())),
                new Vec3(this.r2.dot(rhs.c1()), this.r2.dot(rhs.c2()), this.r2.dot(rhs.c3())),
                new Vec3(this.r3.dot(rhs.c1()), this.r3.dot(rhs.c2()), this.r3.dot(rhs.c3()))
        );
    }

    public Vec3 matmul_vec(Vec3 rhs) {
        return new Vec3(
                r1.dot(rhs),
                r2.dot(rhs),
                r3.dot(rhs)
        );
    }
}
