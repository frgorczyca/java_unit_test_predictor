package org.dtu.analysis.vector;

public class Vec3 {
    public double x;
    public double y;
    public double z;

    public Vec3(double x, double y, double z) {
        this.x = x;
        this.y = y;
        this.z = z;
    }

    public static Vec3 ones() {
        return new Vec3(1, 1, 1);
    }

    public static Vec3 zeros() {
        return new Vec3(0, 0, 0);
    }

    public Vec3 add(Vec3 rhs) {
        return new Vec3(this.x + rhs.x, this.y + rhs.y, this.z + rhs.z);
    }

    public Vec3 add_c(double rhs) {
        return new Vec3(this.x + rhs, this.y + rhs, this.z + rhs);
    }

    public Vec3 sub(Vec3 rhs) {
        return new Vec3(this.x - rhs.x, this.y - rhs.y, this.z - rhs.z);
    }

    public Vec3 sub_c(double rhs) {
        return new Vec3(this.x - rhs, this.y - rhs, this.z - rhs);
    }

    public Vec3 mul(Vec3 rhs) {
        return new Vec3(this.x * rhs.x, this.y * rhs.y, this.z * rhs.z);
    }

    public Vec3 mul_c(double rhs) {
        return new Vec3(this.x * rhs, this.y * rhs, this.z * rhs);
    }

    public Vec3 div(Vec3 rhs) {
        return new Vec3(this.x / rhs.x, this.y / rhs.y, this.z / rhs.z);
    }

    public Vec3 div_c(double rhs) {
        return new Vec3(this.x / rhs, this.y / rhs, this.z / rhs);
    }

    public double dot(Vec3 rhs) {
        return this.x * rhs.x + this.y * rhs.y + this.z * rhs.z;
    }

    public double magnitude() {
        return Math.sqrt(this.dot(this));
    }

    public Vec3 cross(Vec3 rhs) {
        return new Vec3(
                this.y * rhs.z - this.z * rhs.y,
                this.z * rhs.x - this.x * rhs.z,
                this.x * rhs.y - this.y * rhs.x
        );
    }
}
