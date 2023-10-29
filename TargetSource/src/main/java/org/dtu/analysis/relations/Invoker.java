package org.dtu.analysis.relations;

public class Invoker {

    public String label = "default";
    public int number = 0;

    public void InvokeBasic(Basic b){
        number = b.GetId();
    }

    public void InvokeComposed(Composed c){
        label = c.GetLabel();
        number = c.GetIdSum();
    }

    public void InvokeOffspring(Offspring off){
        number = off.GetId();
    }

    public void InvokeOverrider(Overrider ov){
        number = ov.GetIdSum();
        label = ov.GetLabel();
    }
}
