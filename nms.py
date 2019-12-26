def get_IoU(bbox1, bbox2):
    '''
    purpose: return a IoU of bbox1 and bbox2  
    parameter: bbox1 and bbox2 is [x, y, w, h]
    reture: the IOU of bbox1 and bbox2
    ''' 
    # bbox = [x,y,w,h]
    # Calculate the x-y co-ordinates of the rectangles
    x1_tl = bbox1[0]
    x2_tl = bbox2[0]
    x1_br = bbox1[0] + bbox1[2]
    x2_br = bbox2[0] + bbox2[2]
    y1_tl = bbox1[1]
    y2_tl = bbox2[1]
    y1_br = bbox1[1] + bbox1[3]
    y2_br = bbox2[1] + bbox2[3]
    # Calculate the overlapping Area
    x_overlap = max(0, min(x1_br, x2_br)-max(x1_tl, x2_tl))
    y_overlap = max(0, min(y1_br, y2_br)-max(y1_tl, y2_tl))
    overlap_area = x_overlap * y_overlap
    area_1 = bbox1[2] * bbox2[3]
    area_2 = bbox2[2] * bbox2[3]
    total_area = area_1 + area_2 - overlap_area
    return overlap_area / float(total_area)


def nms(detections, threshold=0.5):
    '''
    This function performs Non-Maxima Suppression.
    parameter: `detections`: a list of detections.
                             Each detection is in the format ->
                             [bndbox[x, y, w, h], class, confidence-of-detections,]
                `threshold`: If the IOU is greater than the threshold,
                             the area with the lower confidence score is removed.
    return: a list of detections after NMS.
    '''
    if len(detections) == 0:
	    return []
    # Sort the detections based on confidence score, large to small
    detections = sorted(detections, key=lambda det_dict: max(det_dict["decision_func"][0]), reverse=True)
    # Unique detections will be appended to this list
    new_detections=[]
    # Append the first detection
    new_detections.append(detections[0])
    # Remove the detection from the original list
    del detections[0]
    # For each detection, calculate the overlapping area
    # and if area of overlap is less than the threshold set
    # for the detections in `new_detections`, append the 
    # detection to `new_detections`.
    # In either case, remove the detection from `detections` list.
    for index, detection in enumerate(detections):
        for new_detection in new_detections:
            if get_IoU(detection["bndbox"], new_detection["bndbox"]) > threshold:
                del detections[index]
                break
        else:
            new_detections.append(detection)
            del detections[index]
    # while len(detections):
    #     # Append the first detection
    #     new_detections.append(detections[0])
    #     # Remove the detection from the original list
    #     del detections[0]
    #     # 遍历detections剩余的detection
    #     for index, detection in enumerate(detections):
    #         if get_IoU(detection, new_detections[-1]) > threshold:
    #             del detections[index]
    return new_detections
