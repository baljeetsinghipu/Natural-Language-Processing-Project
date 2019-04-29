
import numpy as np
from collections import OrderedDict
import torch
import torch.nn as nn
class LSTMEncoder(nn.Module):
    def __init__(self, config):
        super(LSTMEncoder, self).__init__()
		
        self.bsize = config['bsize']
        self.word_emb_dim = config['word_emb_dim']
        self.enc_lstm_dim = config['enc_lstm_dim']
        self.pool_type = config['pool_type']
        self.dpout_model = config['dpout_model']
        self.n_lstm_layers = config['n_lstm_layers']

        self.enc_lstm = nn.LSTM(self.word_emb_dim, self.enc_lstm_dim,self.n_lstm_layers,bidirectional=True, dropout=self.dpout_model)

        self.fc = nn.Linear(self.enc_lstm_dim*2, self.enc_lstm_dim)

    def forward(self, sent_tuple):
        # sent_len [max_len, ..., min_len] (batch)
        # sent (seqlen x batch x worddim)

        sent, sent_len = sent_tuple

        # Sort by length (keep idx)
        sent_len, idx_sort = np.ascontiguousarray(np.sort(sent_len)[::-1]), np.argsort(-sent_len)
		
        sent = sent.index_select(1, torch.LongTensor(idx_sort))

        # Handling padding in Recurrent Networks
        sent_packed = nn.utils.rnn.pack_padded_sequence(sent, sent_len)

        _, (hn, _) = self.enc_lstm(sent_packed) # 2 * BatchSize* Enc_lstm_dim

        sent_output = torch.cat((hn[0], hn[1]), dim=1) #bactchsize * encoding dimension * 2
        idx_unsort = np.argsort(idx_sort)
        emb = sent_output.index_select(0, torch.LongTensor(idx_unsort))

        emb = self.fc(emb)

        return emb

class NLINet(nn.Module):
    def __init__(self, config):
        super(NLINet, self).__init__()

        # classifier
        self.nonlinear_fc = config['nonlinear_fc']
        self.fc_dim = config['fc_dim']
        self.n_classes = config['n_classes']
        self.enc_lstm_dim = config['enc_lstm_dim']
        self.encoder_type = config['encoder_type']
        self.dpout_fc = config['dpout_fc']

        self.encoder = eval(self.encoder_type)(config)
        self.inputdim = self.enc_lstm_dim

#            )
        self.classifier = nn.Sequential(
            nn.Linear( self.inputdim, self.fc_dim),
            nn.Dropout(p=self.dpout_fc),
            nn.Linear(self.fc_dim, self.fc_dim),
            nn.Linear(self.fc_dim, self.fc_dim),
            nn.Dropout(p=self.dpout_fc),
            nn.ReLU(),
            nn.Linear(self.fc_dim, self.fc_dim),
            nn.Linear(self.fc_dim, self.n_classes)
            )
        
#        self.classifier = nn.Sequential(
#            nn.Linear( self.inputdim, self.fc_dim),
#            nn.Linear(self.fc_dim, self.fc_dim),
#            nn.Linear(self.fc_dim, self.n_classes)
#            )

    def forward(self, s1):
        # s1 : (s1, s1_len)
        u = self.encoder(s1)
        output = self.classifier(u)
        return output