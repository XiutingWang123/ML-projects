import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.HashMap;
import java.util.LinkedList;

/**
 * Fill in the implementation details of the class DecisionTree using this file. Any methods or
 * secondary classes that you want are fine but we will only interact with those methods in the
 * DecisionTree framework.
 * 
 * You must add code for the 1 member and 4 methods specified below.
 * 
 * See DecisionTree for a description of default methods.
 */
public class DecisionTreeImpl extends DecisionTree {
  private DecTreeNode root;
  //ordered list of class labels
  private List<String> labels; 
  //ordered list of attributes
  private List<String> attributes; 
  //map to ordered discrete values taken by attributes
  private Map<String, List<String>> attributeValues; 
  private static final double EPSILON= 1e-6;
  
  
  /**
   * Answers static questions about decision trees.
   */
  DecisionTreeImpl() {
    // no code necessary this is void purposefully
  }

  /**
   * Build a decision tree given only a training set.
   * 
   * @param train: the training set
   */
  DecisionTreeImpl(DataSet train) {

    this.labels = train.labels;
    this.attributes = train.attributes;
    this.attributeValues = train.attributeValues;
    // TODO: add code here

    List<String> _attributes=new ArrayList<String>();
    for(String attr: attributes)
      _attributes.add(attr);
    
    root=decisionTreeLearning(_attributes, train.instances, null, null);
  }
  
  
  /**
   * The main function to build the decision tree using training set
   */
  public DecTreeNode decisionTreeLearning(List<String> attributes, List<Instance> instances, 
                                          List<Instance> parentInstances, String parentAttrValue)
 {
    DecTreeNode node=null;
    String label=null;
    
    if(instances.size()==0)
    {
      label=pluralityValue(parentInstances);
      node=new DecTreeNode(label,null,parentAttrValue,true);
    }
    
    else if(isSameLabel(instances))
    {
      label=instances.get(0).label;
      node=new DecTreeNode(label,null,parentAttrValue,true);
    }
    
    else if(attributes.size()==0)
    {
      label=pluralityValue(instances);
      node=new DecTreeNode(label,null,parentAttrValue,true);
    }
    
    else
    {
      String A=nextAttribute(instances, attributes);
      label=pluralityValue(instances);
      node=new DecTreeNode(label,A,parentAttrValue,false);
      List<String> attrValues=attributeValues.get(A);
      
      for(String value: attrValues)
      {
        List<Instance> exs_Instances=extractInstances(instances,A,value);   
        List<String> remain_Attributes=remainingAttributes(attributes, A);
        DecTreeNode subtree=decisionTreeLearning(remain_Attributes, exs_Instances, instances, value);
        node.addChild(subtree);              
      }       
    }
    return node;
 }
    
                                          

  /**
   * Build a decision tree given a training set then prune it using a tuning set.
   * 
   * @param train: the training set
   * @param tune: the tuning set
   */
  DecisionTreeImpl(DataSet train, DataSet tune) {

    this.labels = train.labels;
    this.attributes = train.attributes;
    this.attributeValues = train.attributeValues;
    // TODO: add code here
    
    List<String> _attributes=new ArrayList<String>();
    for(String attr: attributes)
      _attributes.add(attr);
    
    DecTreeNode originalTree=decisionTreeLearning(_attributes, train.instances, null, null);
    root=decisionTreePruning(originalTree, tune.instances);
        
  }
  
  
  /**
   * The main function to prune the given decision tree using a tuning set
   */
  public DecTreeNode decisionTreePruning(DecTreeNode originalTree, List<Instance> instances)
  {
    DecTreeNode candTree=originalTree;
    boolean progressMade=true;
    
    while(progressMade)
    {
      List<DecTreeNode> treeNodes=getNodes(candTree);
      double candAcc=accuracy(candTree, instances);
   
      DecTreeNode prunedTree=null;
      DecTreeNode bestTree=null;
      double bestAcc=0.0;
    
      for(DecTreeNode node: treeNodes)
      {
        prunedTree=copyExceptNode(candTree, node);
        double prunedAcc=accuracy(prunedTree, instances);
                   
        if(bestTree==null)     
        {
          bestTree=prunedTree;
          bestAcc=prunedAcc;
        }
      
        else if(prunedAcc>bestAcc)
        {
          bestTree=prunedTree;
          bestAcc=prunedAcc;
        } 
        
      }
     
     
      if    (bestAcc>=candAcc || Math.abs(bestAcc-candAcc)<EPSILON)   candTree=bestTree;
      else  progressMade=false;  
      
    }
    
    return candTree;      
  }  
  
 
  /**
   * Get all the nodes of the given tree using BFS
   */
  public List<DecTreeNode> getNodes(DecTreeNode tree)
  {
    LinkedList<DecTreeNode> queue=new LinkedList<DecTreeNode>(); 
    List<DecTreeNode> nodeSet=new ArrayList<DecTreeNode>();
    
    queue.offer(tree);    
    while(!queue.isEmpty())
    {
      DecTreeNode nd=queue.poll();
      if(!nd.terminal)
      {
        nodeSet.add(nd); 
        List<DecTreeNode> children=nd.children;
        for(DecTreeNode child: children)
          if(!child.terminal)
            queue.offer(child);               
      }
    }
    return nodeSet;
  } 

  
 /**
  * Copy the same tree with the pass-in original tree but lack the given node and its children  
  */
  public DecTreeNode copyExceptNode(DecTreeNode originalTree, DecTreeNode node)
  {
    DecTreeNode copy=null;
    //comparing two nodes using their reference
    if(originalTree!=node)
    {
      copy=new DecTreeNode(originalTree.label,originalTree.attribute,originalTree.parentAttributeValue,originalTree.terminal);
      if(!copy.terminal)
      {
        for(DecTreeNode child: originalTree.children)
          copy.addChild(copyExceptNode(child,node));
      }
    }
    
    else if(originalTree==node)
      copy=new DecTreeNode(originalTree.label,null,originalTree.parentAttributeValue,true);
      
       
    return copy;
  }
  
  
  
  /**
   * Compute the accuracy of the pass-in instances for the given tree 
   */
  public double accuracy(DecTreeNode tree, List<Instance> instances)
  {
    double totalExamples=instances.size();
    double sameCount=0.0;
    
    if(totalExamples==0.0) 
    {
      System.out.println("Instance number is zero, the accuracy can not be computed.");
      System.exit(-1);
    }
    
    for(Instance in:instances)
    {   
      DecTreeNode node=tree;
      while(!node.terminal)
      {
        String attr=node.attribute;
        int attrIndex=getAttributeIndex(attr);
        int attrValueIndex=getAttributeValueIndex(attr, in.attributes.get(attrIndex));
        node=node.children.get(attrValueIndex);
      }
      
      String label=node.label;
      if(label.equals(in.label)) sameCount++;
    }
    
    return sameCount/totalExamples;
    
  }

 
 /**
  * Find the majority label among given instances
  */
 public String pluralityValue(List<Instance> instances)
 {
   int[] count=new int[this.labels.size()];
     
   for(int i=0;i<this.labels.size();i++)
     for(Instance in: instances)    
       if(in.label.equals(this.labels.get(i)))
         count[i]++;  
   
   int maxCount=0;
   String majorLabel=null;
   
   for(int i=0;i<this.labels.size();i++)
   {  
     if(count[i]>maxCount) 
     { 
       maxCount=count[i];
       majorLabel=this.labels.get(i);
     }
   }   
   return majorLabel;  
 }
 
 /**
  * Compute the total entropy of the given instances
  */
 public double totalEntropy(List<Instance> instances)
 {
   double totalExamples=instances.size();
   double[] labelCount=new double[this.labels.size()]; 
   
   double entropy=0.0;
   for(int i=0;i<this.labels.size();i++)
   {
     for(Instance in: instances)
     {
       if(in.label.equals(this.labels.get(i)))
         labelCount[i]++;
     }
     
     if(totalExamples==0)
       entropy+=0.0;
     
     else if((labelCount[i]/totalExamples-0.0) < EPSILON || (1.0-labelCount[i]/totalExamples) <EPSILON)
       entropy+=0.0;
     
     else
       entropy+=-nlog2(labelCount[i]/totalExamples);
   }
  
   return entropy;  
 }
 
 
 /**
  * Compute the specific entropy among the instances that have the same attribute value
  */
 public double entropy(List<Instance> instances, String attr, String decision)
 {
   double[] totalExamples=new double[this.labels.size()]; 
   double[] labelCount=new double[this.labels.size()]; 
   int attrIndex=getAttributeIndex(attr);
   
   double entropy=0.0;
   for(int i=0;i<this.labels.size();i++)
   {
    for(Instance in:instances)
    {
      if(in.attributes.get(attrIndex).equals(decision))
      {
        totalExamples[i]++;
        if(in.label.equals(this.labels.get(i)))
          labelCount[i]++;
      }      
    }    
    
    if(totalExamples[i]==0)
      entropy+=0.0;
    
    else if((labelCount[i]/totalExamples[i]-0.0) < EPSILON || (1.0-labelCount[i]/totalExamples[i]) < EPSILON)
      entropy+=0.0;
      
    else
      entropy+=-nlog2(labelCount[i]/totalExamples[i]); 
   }
     
   return entropy;  
 }
 
 
 /**
  * Compute the information gain among the pass-in-attributes
  */
 public double informationGain(List<Instance> instances, String attr)
 {
     double sum=totalEntropy(instances);
     double totalExamples=instances.size();
     int attrIndex=getAttributeIndex(attr);
     
     if(totalExamples==0) return sum;
     
     List<String> attrValues=this.attributeValues.get(attr);
     double[] decisionCount=new double[attrValues.size()];
     double[] entropyPart=new double[attrValues.size()];
     
     for(int i=0;i<attrValues.size();i++)
     {
       String decision=attrValues.get(i);
       for(Instance in:instances)
       {
         if(in.attributes.get(attrIndex).equals(decision))
           decisionCount[i]++;
       }
       entropyPart[i]=entropy(instances, attr, decision);
       
       if(totalExamples==0)
         sum+=0.0;
       
       else if((decisionCount[i]/totalExamples-0.0) < EPSILON)
         sum+=0.0;
       
       else if((1.0-decisionCount[i]/totalExamples) < EPSILON)
         sum+=-1*entropyPart[i];
         
       else
         sum+=-(decisionCount[i]/totalExamples)*entropyPart[i];
     }
     
     return sum;    
 }
 
 
 public String nextAttribute(List<Instance> instances, List<String> attributes)
 {
   double currentGain=-100.0, bestGain=-100.0;
   String bestAttribute=null;
   
   for(String attr: attributes)
   {
     currentGain=informationGain(instances, attr);
     if(currentGain>bestGain) 
     {
       bestGain=currentGain;
       bestAttribute=attr;
     }
         
   }
   
   return bestAttribute;
 }
 
 
 public List<String> remainingAttributes(List<String> attributes, String attr)
 {
   List<String> result=new ArrayList<String>();
   for(String str: attributes)
   {
     if(!str.equals(attr))
       result.add(str);
   }
   return result;
 }
 
 
 public List<Instance> extractInstances(List<Instance> instances, String attr, String attrValue) 
 {
   List<Instance> extract=new ArrayList<Instance>();
   
   int attrIndex=getAttributeIndex(attr);
   for (Instance in : instances) 
   {
     if(in.attributes.get(attrIndex).equals(attrValue))
         extract.add(in);
   }       
   return extract;
 }
 
 /**
  * Check if all instances have the same label
  */   
 public boolean isSameLabel(List<Instance> instances)
 {
   String labelCheck=instances.get(0).label;
   
   for(Instance in: instances)
   {
     if(!in.label.equals(labelCheck))
       return false;
   }
   return true;
 }
 
 
 public static double nlog2(double value)
 { 
   if(value==0)  return 0;
  
   return value*Math.log(value)/Math.log(2); 
 }
 
 
  
  
  @Override
  public String classify(Instance instance) {

    // TODO: add code here
    String result=null;
    
    DecTreeNode node=root;
    while(!node.terminal)
    {
      String attr=node.attribute;
      int attrIndex=getAttributeIndex(attr);
      int attrValueIndex=getAttributeValueIndex(attr, instance.attributes.get(attrIndex));
      node=node.children.get(attrValueIndex);
    }   
    result=node.label;  
    
    return result;
  }

  @Override
  public void rootInfoGain(DataSet train) {
    this.labels = train.labels;
    this.attributes = train.attributes;
    this.attributeValues = train.attributeValues;
    // TODO: add code here
    
    for(String attr: attributes)
    {
      double gain=informationGain(train.instances, attr);
      System.out.format("%s %.5f%n", attr, gain);
    }
  }
  
  @Override
  /**
   * Print the decision tree in the specified format
   */
  public void print() {

    printTreeNode(root, null, 0);
  }

  /**
   * Prints the subtree of the node with each line prefixed by 4 * k spaces.
   */
  public void printTreeNode(DecTreeNode p, DecTreeNode parent, int k) {
    StringBuilder sb = new StringBuilder();
    for (int i = 0; i < k; i++) {
      sb.append("    ");
    }
    String value;
    if (parent == null) {
      value = "ROOT";
    } else {
      int attributeValueIndex = this.getAttributeValueIndex(parent.attribute, p.parentAttributeValue);
      value = attributeValues.get(parent.attribute).get(attributeValueIndex);
    }
    sb.append(value);
    if (p.terminal) {
      sb.append(" (" + p.label + ")");
      System.out.println(sb.toString());
    } else {
      sb.append(" {" + p.attribute + "?}");
      System.out.println(sb.toString());
      for (DecTreeNode child : p.children) {
        printTreeNode(child, p, k + 1);
      }
    }
  }

  /**
   * Helper function to get the index of the label in labels list
   */
  private int getLabelIndex(String label) {
    for (int i = 0; i < this.labels.size(); i++) {
      if (label.equals(this.labels.get(i))) {
        return i;
      }
    }
    return -1;
  }
 
  /**
   * Helper function to get the index of the attribute in attributes list
   */
  private int getAttributeIndex(String attr) {
    for (int i = 0; i < this.attributes.size(); i++) {
      if (attr.equals(this.attributes.get(i))) {
        return i;
      }
    }
    return -1;
  }

  /**
   * Helper function to get the index of the attributeValue in the list for the attribute key in the attributeValues map
   */
  private int getAttributeValueIndex(String attr, String value) {
    for (int i = 0; i < attributeValues.get(attr).size(); i++) {
      if (value.equals(attributeValues.get(attr).get(i))) {
        return i;
      }
    }
    return -1;
  }
}
