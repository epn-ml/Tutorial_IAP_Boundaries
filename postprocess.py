import crossing as cr

def evaluate(predicted_list, test_list, thres=3):
    '''
    for each cloud of validation_list, gives the list of clouds in the
    predicted_list that overlap the cloud among the threshold
    '''
    #pred = predicted_list
    TP = [x for x in predicted_list if cr.isInList(x, test_list, thres) == True]
    FP = [x for x in predicted_list if cr.isInList(x, test_list, thres) == False]
    
    FN = [x for x in test_list if cr.isInList(x, predicted_list, thres) == False]
    
    print('Precision is:',len(TP)/(len(TP)+len(FP)))
    print('Recall is:',len(TP)/(len(TP)+len(FN)))
    print('True Positives', len(TP))
    print('False Negatives', len(FN))
    print('False Positives', len(FP))
    
    return TP, FN, FP