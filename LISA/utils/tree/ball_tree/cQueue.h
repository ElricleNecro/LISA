#ifndef CQUEUE_H_AP2M8ZUK
#define CQUEUE_H_AP2M8ZUK

#include "cPoint.h"

// a element of a queue
typedef struct _Queue_element {
    Point point;
    double priority;
}* Queue_element;

// a queue
typedef struct _Queue {
    Queue_element buffer;
    unsigned int allocated;
    unsigned int size;
}* Queue;

#include "cNode.h"

// to create a new queue with specified max size
Queue Queue_New(unsigned int size);

// clear queue
void Queue_clear(Queue queue);

// to insert an element in the queue
void Queue_insert(
    Queue queue,
    Point point,
    double priority
);

// append points of node in a queue
void Queue_appendPoints(
    Queue queue,
    Node node,
    Point point_0
);

// return the maximal priority in the queue
double Queue_maxPriority(Queue queue);
double Queue_max(Queue queue);

// search points and add to queue
void Queue_nodeSearch(
    Queue queue,
    Node node,
    Node query
);

// free the memory of the queue
void Queue_free(Queue queue);

#endif /* end of include guard: CQUEUE_H_AP2M8ZUK */

