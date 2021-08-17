from flask import Flask, render_template, request, redirect
import json
import numpy as np
import pandas as pd
import twitter_ext
import tmdb_extraction as tmdbweb

app = Flask(__name__)
key_value = ''


@app.route('/', methods=['get'])
def index():
    return render_template('index.html')


@app.route('/', methods=['post'])
def get_input():
    form = request.form
    if request.form['api']:
        extraction_type = request.form['api']
        keyword = request.form['keyword']

        return render_template('index.html', value=form)


@app.route('/get_tweets', methods=['get'])
def get_tweets():
    quest = request.args.get('quest')
    df = twitter_ext.tweettable(quest)
    sample = []
    for row in df.itertuples():
        sample.append(row)
    tables = {'tables': sample}

    return tables


@app.route('/get_twitter_details', methods=['get'])
def get_twitter_details():
    quest = request.args.get('quest')
    use = request.args.get('use')

    df = twitter_ext.tweettable(quest)
    columns = df.columns.tolist()

    if (use == 'col'):
        cols = {'col': columns}
        json_string = json.dumps(cols)
        return json_string

    if (use == 'stats'):
        col1s = df.columns.tolist()
        col = request.args.get('column')
        summary = request.args.get('summary')
        if (summary == 'All' and col == 'All'):
            l1 = ["Column", "Median", "Sum", "Count", "Mean", "Std", "Nulls", "Distinct count"]
            sample = []
            for col1 in col1s:
                if ((df[col1].dtype == np.int64) or (df[col1].dtype == np.float64)):
                    l2 = [col1, round(df[col1].median(), 2), round(df[col1].sum(), 2), df[col1].count(),
                          round(df[col1].mean(), 2), round(df[col1].std(), 2), df[col1].isna().sum(),
                          df[col1].nunique()]
                    sample.append(l2)
                else:
                    if (type(df[col1][0]) == list):
                        l2 = [col1, "N/A", "N/A", df[col1].count(), "N/A", "N/A", df[col1].isna().sum(), "N/A"]
                        sample.append(l2)
                    elif ((type(df[col1][0]) == str or bool) and (type(df[col1][0]) != float)):
                        l2 = [col1, "N/A", "N/A", df[col1].count(), "N/A", "N/A", df[col1].isna().sum(),
                              df[col1].nunique()]
                        sample.append(l2)
                    else:
                        l2 = [col1, "N/A", "N/A", df[col1].count(), "N/A", "N/A", df[col1].isna().sum(), "N/A"]
                        sample.append(l2)
            tablelist = pd.DataFrame(sample, columns=l1)
            # tablelist.reset_index(drop=True,inplace=True)
            tables = {'tables': tablelist.to_html(index=False)}
            # tables={'tables':"Erroe"}
            json_string = json.dumps(tables)
            return json_string
        if (summary == 'All' and col != 'All'):
            l1 = ["Median", "Sum", "Count", "Mean", "Std", "Nulls", "Distinct count"]
            if ((df[col].dtype == np.int64) or (df[col].dtype == np.float64)):
                l2 = [round(df[col].median(), 2), round(df[col].sum(), 2), df[col].count(), round(df[col].mean(), 2),
                      round(df[col].std(), 2), df[col].isna().sum(), df[col].nunique()]
                tablelist = pd.DataFrame({'column': l1, col: l2})
                tablelist.set_index('column', inplace=True)
                tables = {'tables': tablelist.transpose().to_html()}
            else:
                if (type(df[col][0]) == list):
                    l2 = ["N/A", "N/A", df[col].count(), "N/A", "N/A", "N/A", "N/A"]
                    tablelist = pd.DataFrame({'column': l1, col: l2})
                    tablelist.set_index('column', inplace=True)
                    tables = {'tables': tablelist.transpose().to_html()}
                elif ((type(df[col][0]) == str or bool) and (type(df[col][0]) != float)):
                    l2 = ["N/A", "N/A", df[col].count(), "N/A", "N/A", df[col].isna().sum(), df[col].nunique()]
                    tablelist = pd.DataFrame({'column': l1, col: l2})
                    tablelist.set_index('column', inplace=True)
                    tables = {'tables': tablelist.transpose().to_html()}
                else:
                    l2 = ["N/A", "N/A", df[col].count(), "N/A", "N/A", df[col].isna().sum(), "N/A"]
                    tablelist = pd.DataFrame({'column': l1, col: l2})
                    tablelist.set_index('column', inplace=True)
                    tables = {'tables': tablelist.transpose().to_html()}
            json_string = json.dumps(tables)
            return json_string
        elif (summary != 'All' and col == 'All'):
            l1 = ["column", summary]
            sample = []
            for col in col1s:
                if ((df[col].dtype == np.int64) or (df[col].dtype == np.float64)):
                    if (summary == "Median"):
                        l2 = [col, round(df[col].median(), 2)]
                        sample.append(l2)
                    if (summary == "Sum"):
                        l2 = [col, round(df[col].sum(), 2)]
                        sample.append(l2)
                    if (summary == "Count"):
                        l2 = [col, df[col].count()]
                        sample.append(l2)
                    if (summary == "Mean"):
                        l2 = [col, df[col].mean()]
                        sample.append(l2)
                    if (summary == "Std"):
                        l2 = [col, round(df[col].std(), 2)]
                        sample.append(l2)
                    if (summary == "Nulls"):
                        l2 = [col, df[col].isna().sum()]
                        sample.append(l2)
                    if (summary == "Distinct Count"):
                        l2 = [col, df[col].nunique()]
                        sample.append(l2)
                else:
                    if (type(df[col][0]) == list):
                        if (summary == "Median"):
                            l2 = [col, "N/A"]
                            sample.append(l2)
                        if (summary == "Sum"):
                            l2 = [col, "N/A"]
                            sample.append(l2)
                        if (summary == "Count"):
                            l2 = [col, df[col].count()]
                            sample.append(l2)
                        if (summary == "Mean"):
                            l2 = [col, "N/A"]
                            sample.append(l2)
                        if (summary == "Std"):
                            l2 = [col, "N/A"]
                            sample.append(l2)
                        if (summary == "Nulls"):
                            l2 = [col, "N/a"]
                            sample.append(l2)
                        if (summary == "Distinct Count"):
                            l2 = [col, "N/A"]
                            sample.append(l2)
                    elif ((type(df[col][0]) == str or bool) and (type(df[col][0]) != float)):
                        if (summary == "Median"):
                            l2 = [col, "N/A"]
                            sample.append(l2)
                        if (summary == "Sum"):
                            l2 = [col, "N/A"]
                            sample.append(l2)
                        if (summary == "Count"):
                            l2 = [col, df[col].count()]
                            sample.append(l2)
                        if (summary == "Mean"):
                            l2 = [col, "N/A"]
                            sample.append(l2)
                        if (summary == "Std"):
                            l2 = [col, "N/A"]
                            sample.append(l2)
                        if (summary == "Nulls"):
                            l2 = [col, df[col].isna().sum()]
                            sample.append(l2)
                        if (summary == "Distinct Count"):
                            l2 = [col, df[col].nunique()]
                            sample.append(l2)
                    else:
                        if (summary == "Median"):
                            l2 = [col, "N/A"]
                            sample.append(l2)
                        if (summary == "Sum"):
                            l2 = [col, "N/A"]
                            sample.append(l2)
                        if (summary == "Count"):
                            l2 = [col, df[col].count()]
                            sample.append(l2)
                        if (summary == "Mean"):
                            l2 = [col, "N/A"]
                            sample.append(l2)
                        if (summary == "Std"):
                            l2 = [col, "N/A"]
                            sample.append(l2)
                        if (summary == "Nulls"):
                            l2 = [col, df[col].isna().sum()]
                            sample.append(l2)
                        if (summary == "Distinct Count"):
                            l2 = [col, "N/A"]
                            sample.append(l2)

            tablelist = pd.DataFrame(sample, columns=l1)
            # tablelist.reset_index(drop=True,inplace=True)
            tables = {'tables': tablelist.to_html(
                index=False)}  # tables={'tables':'<h3>Column data type is not String or Integer or Float </h3>'}
            json_string = json.dumps(tables)
            return json_string
        else:
            l1 = [summary]
            if ((df[col].dtype == np.int64) or (df[col].dtype == np.float64)):
                if (summary == "Median"):
                    l2 = [round(df[col].median(), 2)]
                if (summary == "Sum"):
                    l2 = [round(df[col].sum(), 2)]
                if (summary == "Count"):
                    l2 = [df[col].count()]
                if (summary == "Mean"):
                    l2 = [df[col].mean()]
                if (summary == "Std"):
                    l2 = [round(df[col].std(), 2)]
                if (summary == "Nulls"):
                    l2 = [df[col].isna().sum()]
                if (summary == "Distinct Count"):
                    l2 = [df[col].nunique()]
                tablelist = pd.DataFrame({'column': l1, col: l2})
                tablelist.set_index('column', inplace=True)
                tables = {'tables': tablelist.transpose().to_html()}
            else:
                if (type(df[col][0]) == list):
                    if (summary == "Median"):
                        l2 = ["N/A"]
                    if (summary == "Sum"):
                        l2 = ["N/A"]
                    if (summary == "Count"):
                        l2 = [df[col].count()]
                    if (summary == "Mean"):
                        l2 = ["N/A"]
                    if (summary == "Std"):
                        l2 = ["N/A"]
                    if (summary == "Nulls"):
                        l2 = ["N/A"]
                    if (summary == "Distinct Count"):
                        l2 = ["N/A"]
                    tablelist = pd.DataFrame({'column': l1, col: l2})
                    tablelist.set_index('column', inplace=True)
                    tables = {'tables': tablelist.transpose().to_html()}
                    # tables={'tables':'<h3>Column data type is not String or Integer or Float </h3>'}
                elif ((type(df[col][0]) == str or bool) and (type(df[col][0]) != float)):
                    if (summary == "Median"):
                        l2 = ["N/A"]
                    if (summary == "Sum"):
                        l2 = ["N/A"]
                    if (summary == "Count"):
                        l2 = [df[col].count()]
                    if (summary == "Mean"):
                        l2 = ["N/A"]
                    if (summary == "Std"):
                        l2 = ["N/A"]
                    if (summary == "Nulls"):
                        l2 = [df[col].isna().sum()]
                    if (summary == "Distinct Count"):
                        l2 = [df[col].nunique()]
                    tablelist = pd.DataFrame({'column': l1, col: l2})
                    tablelist.set_index('column', inplace=True)
                    tables = {'tables': tablelist.transpose().to_html()}
                else:
                    if (summary == "Median"):
                        l2 = ["N/A"]
                    if (summary == "Sum"):
                        l2 = ["N/A"]
                    if (summary == "Count"):
                        l2 = [df[col].count()]
                    if (summary == "Mean"):
                        l2 = ["N/A"]
                    if (summary == "Std"):
                        l2 = ["N/A"]
                    if (summary == "Nulls"):
                        l2 = [df[col].isna().sum()]
                    if (summary == "Distinct Count"):
                        l2 = ["N/A"]
                    tablelist = pd.DataFrame({'column': l1, col: l2})
                    tablelist.set_index('column', inplace=True)
                    tables = {'tables': tablelist.transpose().to_html()}
                    # tables={'tables':'<h3>Column data type is not String or Integer or Float </h3>'}
            json_string = json.dumps(tables)
            return json_string


@app.route('/get_tmdb_details',methods=['get']) 
def get_tmdb_details():
    quest=request.args.get('quest')
    use=request.args.get('use')
    if(use=='col'):
        df= tmdbweb.tmdbtable(quest)
        columns= df.columns.tolist()
        #print(columns)
        cols={'col':columns}
        #print(col)
        json_string = json.dumps(cols)
        return json_string
    if(use=='stats'):
        df= tmdbweb.tmdbtable(quest)
        col1s= df.columns.tolist()
        col=request.args.get('column')
        summary=request.args.get('summary')
        if(summary=='All' and col=='All'):
            l1=["Column","Median","Sum","Count","Mean","Std","Nulls","Distinct count"]
            sample=[]
            for col1 in col1s:
                if ((df[col1].dtype == np.int64) or (df[col1].dtype == np.float64)):
                    l2=[col1,round(df[col1].median(),2),round(df[col1].sum(),2),df[col1].count(),round(df[col1].mean(),2),round(df[col1].std(),2),df[col1].isna().sum(),df[col1].nunique()]
                    sample.append(l2)               
                else:
                    if(type(df[col1][0])==list):
                        l2=[col1,"N/A","N/A",df[col1].count(),"N/A","N/A",df[col1].isna().sum(),"N/A"]
                        sample.append(l2)
                    elif((type(df[col1][0]) == str or bool) and (type(df[col1][0])!= float)): 
                        l2=[col1,"N/A","N/A",df[col1].count(),"N/A","N/A",df[col1].isna().sum(),df[col1].nunique()]
                        sample.append(l2)
                    else:
                        # print("inside others",col1,type(df[col1][0]))
                        l2=[col1,"N/A","N/A",df[col1].count(),"N/A","N/A",df[col1].isna().sum(),"N/A"]
                        sample.append(l2)
            tablelist=pd.DataFrame(sample,columns=l1)
            # tablelist.reset_index(drop=True,inplace=True)
            tables={'tables':tablelist.to_html(index=False)}
          
            json_string = json.dumps(tables)
            return json_string
        if(summary=='All'and col != 'All'):
            l1=["Median","Sum","Count","Mean","Std","Nulls","Distinct count"]
            if ((df[col].dtype == np.int64) or (df[col].dtype == np.float64)):
                l2=[round(df[col].median(),2),round(df[col].sum(),2),df[col].count(),round(df[col].mean(),2),round(df[col].std(),2),df[col].isna().sum(),df[col].nunique()]
                tablelist = pd.DataFrame({'column': l1,col: l2})
                tablelist.set_index('column',inplace=True)
                tables={'tables':tablelist.transpose().to_html()}
            else:
                if(type(df[col][0])==list):
                    l2=["N/A","N/A",df[col].count(),"N/A","N/A",df[col].isna().sum(),"N/A"]
                    tablelist = pd.DataFrame({'column': l1,col: l2})
                    tablelist.set_index('column',inplace=True)
                    tables={'tables':tablelist.transpose().to_html()}
                elif((type(df[col][0])==str or bool)and (type(df[col][0])!= float)):
                    l2=["N/A","N/A",df[col].count(),"N/A","N/A",df[col].isna().sum(),df[col].nunique()]
                    tablelist = pd.DataFrame({'column': l1,col: l2})
                    tablelist.set_index('column',inplace=True)
                    tables={'tables':tablelist.transpose().to_html()}
                else:
                    l2=["N/A","N/A",df[col].count(),"N/A","N/A",df[col].isna().sum(),"N/A"]
                    tablelist = pd.DataFrame({'column': l1,col: l2})
                    tablelist.set_index('column',inplace=True)
                    tables={'tables':tablelist.transpose().to_html()}
                    
            json_string = json.dumps(tables)
            return json_string
        elif(summary!='All'and col=='All'):
            l1=["column",summary]
            sample=[]
            for col in col1s:
                if ((df[col].dtype == np.int64) or (df[col].dtype == np.float64)):
                    if(summary=="Median"):
                        l2=[col,round(df[col].median(),2)]
                        sample.append(l2)
                    if(summary=="Sum"):
                        l2=[col,round(df[col].sum(),2)]
                        sample.append(l2)
                    if(summary=="Count"):
                        l2=[col,df[col].count()]
                        sample.append(l2)
                    if(summary=="Mean"):
                        l2=[col,df[col].mean()]
                        sample.append(l2)
                    if(summary=="Std"):
                        l2=[col,round(df[col].std(),2)]
                        sample.append(l2)
                    if(summary=="Nulls"):
                        l2=[col,df[col].isna().sum()]
                        sample.append(l2)
                    if(summary=="Distinct Count"):
                        l2=[col,df[col].nunique()]
                        sample.append(l2)
                else:
                    if(type(df[col][0])==list):
                        if(summary=="Median"):
                            l2=[col,"N/A"]
                            sample.append(l2)
                        if(summary=="Sum"):
                            l2=[col,"N/A"]
                            sample.append(l2)
                        if(summary=="Count"):
                            l2=[col,df[col].count()]
                            sample.append(l2)
                        if(summary=="Mean"):
                            l2=[col,"N/A"]
                            sample.append(l2)
                        if(summary=="Std"):
                            l2=[col,"N/A"]
                            sample.append(l2)
                        if(summary=="Nulls"):
                            l2=[col,"N/a"]
                            sample.append(l2)
                        if(summary=="Distinct Count"):
                            l2=[col,"N/A"]
                            sample.append(l2)
                    elif((type(df[col][0])==str or bool)and (type(df[col][0])!= float)):
                        if(summary=="Median"):
                            l2=[col,"N/A"]
                            sample.append(l2)
                        if(summary=="Sum"):
                            l2=[col,"N/A"]
                            sample.append(l2)
                        if(summary=="Count"):
                            l2=[col,df[col].count()]
                            sample.append(l2)
                        if(summary=="Mean"):
                            l2=[col,"N/A"]
                            sample.append(l2)
                        if(summary=="Std"):
                            l2=[col,"N/A"]
                            sample.append(l2)
                        if(summary=="Nulls"):
                            l2=[col,df[col].isna().sum()]
                            sample.append(l2)
                        if(summary=="Distinct Count"):
                            l2=[col,df[col].nunique()]
                            sample.append(l2)
                    else:
                        if(summary=="Median"):
                            l2=[col,"N/A"]
                            sample.append(l2)
                        if(summary=="Sum"):
                            l2=[col,"N/A"]
                            sample.append(l2)
                        if(summary=="Count"):
                            l2=[col,df[col].count()]
                            sample.append(l2)
                        if(summary=="Mean"):
                            l2=[col,"N/A"]
                            sample.append(l2)
                        if(summary=="Std"):
                            l2=[col,"N/A"]
                            sample.append(l2)
                        if(summary=="Nulls"):
                            l2=[col,df[col].isna().sum()]
                            sample.append(l2)
                        if(summary=="Distinct Count"):
                            l2=[col,"N/A"]
                            sample.append(l2)
                        
            tablelist=pd.DataFrame(sample,columns=l1)
            
            tables={'tables':tablelist.to_html(index=False)}            # tables={'tables':'<h3>Column data type is not String or Integer or Float </h3>'}
            json_string = json.dumps(tables)
            return json_string
        else:
            l1=[summary]
            if ((df[col].dtype == np.int64) or (df[col].dtype == np.float64)):
                if(summary=="Median"):
                    l2=[round(df[col].median(),2)]
                if(summary=="Sum"):
                    l2=[round(df[col].sum(),2)]
                if(summary=="Count"):
                    l2=[df[col].count()]
                if(summary=="Mean"):
                    l2=[df[col].mean()]
                if(summary=="Std"):
                    l2=[round(df[col].std(),2)]
                if(summary=="Nulls"):
                    l2=[df[col].isna().sum()]
                if(summary=="Distinct Count"):
                    l2=[df[col].nunique()]
                tablelist = pd.DataFrame({'column': l1,col: l2})
                tablelist.set_index('column',inplace=True)
                tables={'tables':tablelist.transpose().to_html()}
            else:
                if(type(df[col][0])==list):
                    if(summary=="Median"):
                        l2=["N/A"]
                    if(summary=="Sum"):
                        l2=["N/A"]
                    if(summary=="Count"):
                        l2=[df[col].count()]
                    if(summary=="Mean"):
                        l2=["N/A"]
                    if(summary=="Std"):
                        l2=["N/A"]
                    if(summary=="Nulls"):
                        l2=["N/a"]
                    if(summary=="Distinct Count"):
                        l2=["N/A"]
                    tablelist = pd.DataFrame({'column': l1,col: l2})
                    tablelist.set_index('column',inplace=True)
                    tables={'tables':tablelist.transpose().to_html()}
                    # tables={'tables':'<h3>Column data type is not String or Integer or Float </h3>'}
                elif((type(df[col][0])==str or bool)and (type(df[col][0])!= float)):
                    if(summary=="Median"):
                        l2=["N/A"]
                    if(summary=="Sum"):
                        l2=["N/A"]
                    if(summary=="Count"):
                        l2=[df[col].count()]
                    if(summary=="Mean"):
                        l2=["N/A"]
                    if(summary=="Std"):
                        l2=["N/A"]
                    if(summary=="Nulls"):
                        l2=[df[col].isna().sum()]
                    if(summary=="Distinct Count"):
                        l2=[df[col].nunique()]
                    tablelist = pd.DataFrame({'column': l1,col: l2})
                    tablelist.set_index('column',inplace=True)
                    tables={'tables':tablelist.transpose().to_html()}
                else:
                    if(summary=="Median"):
                        l2=["N/A"]
                    if(summary=="Sum"):
                        l2=["N/A"]
                    if(summary=="Count"):
                        l2=[df[col].count()]
                    if(summary=="Mean"):
                        l2=["N/A"]
                    if(summary=="Std"):
                        l2=["N/A"]
                    if(summary=="Nulls"):
                        l2=[df[col].isna().sum()]
                    if(summary=="Distinct Count"):
                        l2=["N/A"]
                    tablelist = pd.DataFrame({'column': l1,col: l2})
                    tablelist.set_index('column',inplace=True)
                    tables={'tables':tablelist.transpose().to_html()}
                    # tables={'tables':'<h3>Column data type is not String or Integer or Float </h3>'}
            json_string = json.dumps(tables)
            return json_string


if __name__ == '__main__':
    app.debug = True
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()
    app.run(debug=True)
