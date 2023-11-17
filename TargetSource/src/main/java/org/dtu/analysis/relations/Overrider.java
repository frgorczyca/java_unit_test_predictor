package org.dtu.analysis.relations;

public class Overrider extends Composed {
    public Overrider(Basic b, Offspring off){
        super(b, off);
    }

    @Override
    public String GetLabel() {
        return "L3";
    }
}
