import os
import pandas as pd
import filedialog

class playerinfo():
    ''' loads all dataframes with player info, teams, etc. '''
    def __init__(self, *args, **kwargs):
        self.path = filedialog.askdirectory() 
        # open files 
        
        self.players=None
        self.famcontact=None
        self.masterSUs=None
        self.teams=None
        self.unilist=None
        self.open_main_files() # loads above
    
    def open_main_files(self):
        ''' Auto loads player & family contact info, teams/coaches, master signups
        unilog info '''
        if os.path.exists('players.csv'):
            self.players=pd.read_csv('players.csv', encoding='cp437')
        else:
            print('players.csv not found.')
            self.players=pd.DataFrame()
        if os.path.exists('family_contact.csv'):
            self.famcontact=pd.read_csv('family_contact.csv', encoding='cp437')
        else:
            self.famcontact=pd.DataFrame()
        if os.path.exists('Teams_coaches.xlsx'):
            self.teams=pd.read_excel('Teams_coaches.xlsx', sheetname='Teams')
            self.coaches=pd.read_excel('Teams_coaches.xlsx', sheetname='Coaches') # load coach info
        else:
            self.teams=pd.DataFrame()
            self.coaches=pd.DataFrame()
        if os.path.exists('master_signups.csv'):
            self.mastersignups=pd.read_csv('master_signups.csv', encoding='cp437')
        else:
            self.mastersignups=pd.DataFrame()
        if os.path.exists('Integquantlog.csv'):
            self.Integquantlog=pd.read_csv('Integquantlog.csv', encoding='cp437')
        else:
            self.Integquantlog=pd.DataFrame()
        # Print TEM or SEM to console based on beam kV
        try:
            self.AESquantparams=pd.read_csv('C:\\Users\\tkc\\Documents\\Python_Scripts\\Augerquant\\Params\\AESquantparams.csv', encoding='utf-8')
        except:
            self.AESquantparams=pd.DataFrame()
 

    def get_peakinfo(self):
        ''' takes element strings and energies of background regs and returns tuple for each elem symbol containing all params necessary to find each Auger peak from given spe file 
        also returns 2-tuple with energy val and index of chosen background regions
        ''' 
        # elemental lines (incl Fe2, Fe1, etc.)
        self.peaks=self.Smdifpeakslog.PeakID.unique()
        self.peakdata=[]

        for peak in self.peaks:
            try:
                # find row in AESquantparams for this element
                thispeakdata=self.AESquantparams[(self.AESquantparams['element']==peak)]
                thispeakdata=thispeakdata.squeeze() # series with this elements params
                # return list of length numelements with 5-tuple for each containing 
                # 1) peak symbol, 2) ideal negpeak (eV)  3) ideal pospeak (in eV) 
                # 4)sensitivity kfactor.. and 5) error in kfactor
        
                peaktuple=(peak, thispeakdata.negpeak, thispeakdata.pospeak, 
                           thispeakdata.kfactor, thispeakdata.errkf1) # add tuple with info for this element     
                self.peakdata.append(peaktuple)
            except:
                print('AESquantparams not found for ', peak)
        print('Found', len(self.peakdata), 'quant peaks in smdifpeakslog' )

