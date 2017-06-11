import java.util.HashMap;
import java.util.Map;


/**
 * Your implementation of a naive bayes classifier. Please implement all four methods.
 */

public class NaiveBayesClassifierImpl implements NaiveBayesClassifier {

  /**
   * Trains the classifier with the provided training data and vocabulary size
   */
 
   
  private Map<Label, Map<String, Integer>> wordTypeCount = null;;
  private Map<Label, Integer> labelCount = null;
  private Map<Label, Integer> labelWordsCount = null;
  
  private final Label l0 = Label.SPORTS;
  private final Label l1 = Label.BUSINESS; 
  private final double delta = 0.00001;
  private int vocabularySize = 0;
  private int trainingSize = 0;
  
  
  
  @Override
  public void train(Instance[] trainingData, int v) {
    // TODO : Implement
    
    this.vocabularySize = v; 
    this.trainingSize = trainingData.length;
    
    this.labelCount = new HashMap<Label, Integer>();
    this.labelCount.put(l0, countLabelNum(trainingData, l0));
    this.labelCount.put(l1, countLabelNum(trainingData, l1));
    
    this.labelWordsCount = new HashMap<Label, Integer>();
    this.labelWordsCount.put(l0, countWordsNum(trainingData, l0));
    this.labelWordsCount.put(l1, countWordsNum(trainingData, l1));
    
    this.wordTypeCount = new HashMap<Label, Map<String, Integer>>();
    this.wordTypeCount.put(l0, getWordTypeNum(trainingData, l0));
    this.wordTypeCount.put(l1, getWordTypeNum(trainingData, l1));
    
    
    //System.out.println("sportsMap:" + sportsMap.entrySet());
    //System.out.println("BussinessMap:" + businessMap.entrySet());
       
         
  }
  
 
  public Map<String, Integer> getWordTypeNum(Instance[] trainingData, Label label)
  {   
    Map<String, Integer> wordTypeMap= new HashMap<String, Integer>();
        
    for(int i=0;i<trainingData.length;i++)
    {
      if(trainingData[i].label.equals(label))
      {
        String[] words = trainingData[i].words;           
        for(int j=0;j<words.length;j++)
        {
          if  (wordTypeMap.containsKey(words[j])) wordTypeMap.put(words[j], wordTypeMap.get(words[j])+1);
          else                                    wordTypeMap.put(words[j], 1);
        }
      }
    }
    
    return wordTypeMap;
    
  }
  
 
  
  
  public int countLabelNum(Instance[] trainingData, Label label)
  {
    int count=0;   
    
    for(int i=0;i<trainingData.length;i++)  
      if(trainingData[i].label.equals(label))
        count++;
       
    return count;
  }
  
  
  public int countWordsNum(Instance[] trainingData, Label label)
  {
    int count=0;
    
    for(int i=0;i<trainingData.length;i++)   
      if(trainingData[i].label.equals(label))     
        count+=trainingData[i].words.length;
      
   return count; 
  }

  /*
   * Prints out the number of documents for each label
   */
  public void documents_per_label_count(){
    // TODO : Implement
    
    System.out.println("SPORTS=" + labelCount.get(l0));
    System.out.println("BUSINESS=" + labelCount.get(l1));
    
  }

  /*
   * Prints out the number of words for each label
   */
  public void words_per_label_count(){
    // TODO : Implement
    
    System.out.println("SPORTS=" + labelWordsCount.get(l0));
    System.out.println("BUSINESS=" + labelWordsCount.get(l1));
  }

  /**
   * Returns the prior probability of the label parameter, i.e. P(SPAM) or P(HAM)
   */
  @Override
  public double p_l(Label label) {
    // TODO : Implement
    
    double count = labelCount.get(label);
    
    if  (trainingSize==0) return 0;
    else                  return count/trainingSize;
 
  }

  /**
   * Returns the smoothed conditional probability of the word given the label, i.e. P(word|SPORTS) or
   * P(word|BUSINESS)
   */
  @Override
  public double p_w_given_l(String word, Label label) {
    // TODO : Implement
    
    Map<String, Integer> wordTypeMap = wordTypeCount.get(label);
    double count = 0.0;
    double labelCount = this.labelWordsCount.get(label);
    
    if(wordTypeMap.get(word)!=null)   count = wordTypeMap.get(word);
    
    
    if(this.vocabularySize == 0.0) 
      return  0.0;
    
    else
      return  (count + delta) / (this.vocabularySize*delta + labelCount);
        
  }

  /**
   * Classifies an array of words as either SPAM or HAM.
   */
  @Override
  public ClassifyResult classify(String[] words) {
    // TODO : Implement
    
    ClassifyResult result = new ClassifyResult();
    double Pr_l0 = Math.log(p_l(l0));
    double Pr_l1 = Math.log(p_l(l1));
    
    for(int i=0;i<words.length;i++)
    {
      Pr_l0 += Math.log(p_w_given_l(words[i], l0));
      Pr_l1 += Math.log(p_w_given_l(words[i], l1));
    }
    
    result.log_prob_sports = Pr_l0;
    result.log_prob_business = Pr_l1;
    
    if(Pr_l0 > Pr_l1) result.label = l0;
    else              result.label = l1;
    
    return result;
  }
  
  /*
   * Constructs the confusion matrix
   */
  @Override
  public ConfusionMatrix calculate_confusion_matrix(Instance[] testData){
    // TODO : Implement
    
    int TP = 0; int FP = 0; 
    int FN = 0; int TN = 0;
    
    for(int i=0;i<testData.length;i++)
    {
      Label classifiedLabel = classify(testData[i].words).label;
      
      if(testData[i].label.equals(classifiedLabel))
      {
        if  (classifiedLabel==l0) TP++;
        else                      TN++;
      }
      else
      {
        if  (classifiedLabel==l0) FP++;
        else                      FN++;
      }
    }
       
    return new ConfusionMatrix(TP, FP, FN, TN);
  }
  
}
