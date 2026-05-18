#include "sort_bus_lines.h"


void swap_buses(BusLine *a, BusLine *b) {
    BusLine temp = *a;
    *a = *b;
    *b = temp;
}


void bus_bubble_sort(BusLine *start, BusLine *end) {
    for (BusLine *i = start; i <= end; i++) {
        for (BusLine *j = start; j < end - (i - start); j++) {
            if (strcmp(j->name, (j + 1)->name) > 0) {
                swap_buses(j, j + 1);
            }
        }
    }
}


BusLine *partition(BusLine *start, BusLine *end, SortType sort_type) {
    BusLine *pivot = end;
    BusLine *i = start - 1;

    for (BusLine *j = start; j < end; j++) {
        int comparison = 0;
        if (sort_type == DISTANCE) {
            comparison = (j->distance <= pivot->distance);
        } else if (sort_type == DURATION) {
            comparison = (j->duration <= pivot->duration);
        } else if (sort_type == FREQUENCY) {
            comparison = (j->frequency <= pivot->frequency);
        }

        if (comparison) {
            i++;
            swap_buses(i, j);
        }
    }
    swap_buses(i + 1, end);
    return (i + 1);
}


void bus_quick_sort(BusLine *start, BusLine *end, SortType sort_type) {
    if (start < end) {
        BusLine *pivot = partition(start, end, sort_type);
        bus_quick_sort(start, pivot - 1, sort_type);
        bus_quick_sort(pivot + 1, end, sort_type);
    }
}