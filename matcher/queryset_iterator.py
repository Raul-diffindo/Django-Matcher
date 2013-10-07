import gc


class QuerySetIterator(object):

    def __init__(self, queryset):
        self.__queryset = queryset

    def queryset_iterator(self, chunksize=1000):
        '''
        Iterate over a Django Queryset ordered by the primary key

        This method loads a maximum of chunksize (default: 1000) rows in it's
        memory at the same time while django normally would load all rows in it's
        memory. Using the iterator() method only causes it to not preload all the
        classes.

        Note that the implementation of the iterator does not support ordered query sets.
        '''
        pk = 0
        last_pk = self.__queryset.order_by('-pk')[0].pk
        queryset = self.__queryset.order_by('pk')
        while pk < last_pk:
            for row in queryset.filter(pk__gt=pk)[:chunksize]:
                pk = row.pk
                yield row
            gc.collect()
