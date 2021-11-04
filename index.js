const {PythonShell} = require('python-shell');
const electron = require('electron');
const app = electron.app;
const BrowserWindow = electron.BrowserWindow;
let mainWindow;

// アプリを閉じた時にquit
app.on('window-all-closed', function() {
  app.quit();
});

// アプリ起動後の処理
app.on('ready', function() {
  const rq = require('request-promise');
  const mainAddr = 'http://localhost:5000';
  var pyshell = new PythonShell('./app.py');

  const openWindow = function() {
    mainWindow = new BrowserWindow({width: 1600, height: 1000 });
    mainWindow.loadURL(mainAddr);

    // 開発ツールを有効化
    mainWindow.webContents.openDevTools();

    // 終了処理
    mainWindow.on('closed', function() {

      // キャッシュを削除
      electron.session.defaultSession.clearCache(() => {})
      mainWindow = null;

      pyshell.childProcess.kill('SIGINT');
    });
  };

  const startUp = function() {
    rq(mainAddr)
      .then(function(htmlString) {
        console.log('server started');
        openWindow();
      })
      .catch(function(err) {
        startUp();
      });
  };

  startUp();
});

