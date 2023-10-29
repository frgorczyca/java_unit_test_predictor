package org.dtu.analysis.relations;

public class Composed {
    public Composed(Basic b, Offspring off) {
        this.b = b;
        this.off = off;
    }

    public Basic b;
    public Offspring off;

    public int GetIdSum() {
        return this.b.GetId() + this.off.GetOffsetId();
    }

    public String GetLabel(){
        return BaseMapping.L1.label;
    }
}
