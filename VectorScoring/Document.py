class Document:
    def __init__(self, tup_zero):
        self.short_name = tup_zero[2]
        self.summary_1 = tup_zero[6]
        self.summary_2 = tup_zero[7]
        self.summary_3 = tup_zero[8]
        self.texts = [{'id': tup_zero[0],
                       'blend_id': tup_zero[1],
                       'row_number': tup_zero[9],
                       'row_text': tup_zero[10],
                       'stnd_row_text': tup_zero[11]}]

    def __str__(self):
        pass

    def add_text_row(self, tup_new):
        self.texts.append({'id': tup_new[0],
                           'blend_id': tup_new[1],
                           'row_number': tup_new[9],
                           'row_text': tup_new[10],
                           'stnd_row_text': tup_new[11]})
