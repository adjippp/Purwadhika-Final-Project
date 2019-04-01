from flask import Flask, render_template, json, request,redirect,url_for,flash,session,jsonify,abort,make_response
import loginForm as lf
import registerToCSV as reg
import plottingData as pltd
import utama
import recomm
import search as sr

app = Flask(__name__)
app.secret_key = 'rahasia'
login=False

@app.route("/")
def main():
    popularity=recomm.getPopularity()
    return render_template('index.html',isiPop=popularity)
 
@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/showSignIn')
def showSignIn():
    return render_template('signin.html')

@app.route('/showPlot')
def showPlot():
    grafiks=pltd.build_graph(pltd.cek,pltd.cek2)
    return render_template('plotting.html',grafik=grafiks)

@app.route('/suksesdaftar')
def suksesdaftar():
    return render_template('suksesdaftar.html')

@app.route('/gagaldaftar')
def gagaldaftar():
    return render_template('gagaldaftar.html')

@app.route('/signUp',methods=['POST'])
def signUp():
    namanya = request.form['inputNama']
    usernm= request.form['inputUsername']
    passwd= request.form['inputPassword']
    if reg.register(usernm,passwd,namanya) == False:
        flash('ID atau Password Sudah terdaftar')
        return redirect(url_for('gagaldaftar'))
    else:
        flash('Anda Berhasil Terdaftar')
        return redirect(url_for('suksesdaftar'))

@app.route('/signIn',methods=['GET','POST'])
def signIn():
    error=None
    usernm=request.form['inputUsername']
    passwd=request.form['inputPassword']
    if lf.login(usernm,passwd)==False:
        error = 'Invalid credentials'
        flash('Wrong Username or Password')
    else:
        flash('You were successfully logged in')
        utama.login=True
        return redirect(url_for('index'))
    return render_template('signin.html', error=error)

@app.route('/index')
def index():
    if(utama.login==True):
        nama=lf.getName()
        custId=lf.getID()
        isiPop=recomm.getPopularity()
        isirecomm=recomm.getSimilarity(int(custId))
        return render_template('index2.html',nama=nama,custId=custId,isiPop=isiPop,isirekom=[isirecomm.to_html()])
    else:
        return render_template('belumlogin.html')



@app.route('/search',methods=['POST'])
def search():
    if(utama.login==True):
        nama=lf.getName()
        srch=request.form['search']
        datasearch=sr.searchProduk(srch)
        return render_template('search2.html',nama=nama,df=[datasearch.to_html()],titles=datasearch.columns.values) #atau bisa dengan data={'sesuatu':isi,'sesuatu2':isi2}
    else:
        srch=request.form['search']
        datasearch=sr.searchProduk(srch)
        return render_template('search.html',df=[datasearch.to_html()],titles=datasearch.columns.values)

@app.route('/showPlot2')
def showPlot2():
    if(utama.login==True):
        nama=lf.getName()
        grafiks=pltd.build_graph(pltd.cek,pltd.cek2)
        return render_template('plotting2.html',grafik=grafiks,nama=nama) #atau bisa dengan data={'sesuatu':isi,'sesuatu2':isi2}
    else:
        return render_template('belumlogin.html')
'''
dalam app.route dapat dilakukan
@app.route('/sesuatu/<string:x>)
def sesuatu(x):
    return x
'''
'''
request arguments
contoh /sesuatu?parameter=x
if 'sesuatu' in request.args:    
    id = int(request.args['id'])
    if id ada:
        return sesuatu
    else:
        return abort(404)
else:
    return abort(404)
'''
@app.route('/signOut')
def signOut():
    utama.login=False
    return redirect(url_for('main'))

@app.errorhandler(404)
def notFound(error):
    return make_response(
        jsonify({'Status':'Maaf URL tidak ditemukan.'}),404
    )
#dapat dilakukan dengan mengecek dan return abort(404)
if __name__ == "__main__":
    app.run(debug=True)