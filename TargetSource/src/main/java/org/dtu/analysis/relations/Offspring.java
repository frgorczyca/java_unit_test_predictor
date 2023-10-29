package org.dtu.analysis.relations;

public class Offspring extends Basic {
    public Offspring(int offset){
        this.offset = offset;
    }

    public int offset;

    public int GetOffsetId(){
        return this.id + offset;
    }
}
