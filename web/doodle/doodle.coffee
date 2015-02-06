app = angular.module 'DoodleApp', ['websocket']

app.value 'wsPort', 1111 # websocket need not be on same server as static files

app.controller 'DoodleCtrl', ($scope, $timeout, $websocket, wsPort, fileReader) ->
  wsProto = if "https:" is document.location.protocol then "wss" else "ws"
  ws = $websocket.connect "#{wsProto}://#{location.hostname}:#{wsPort}/ws"

  ws.register '', (topic, body) ->
    console.log 'mqtt:', topic, body

  ws.emit '/doodle', [1, 2, 3]

  $timeout ->
    ws.emit '/doodledah', [4, 5, 6]
  , 1000
  $timeout ->
    ws.emit '/doodle/dah', [7, 8, 9]
  , 2000

  $scope.connect = -> console.log 'CONNECT'

  $scope.disconnect = -> console.log 'DISCONNECT'

  $scope.upload = ->
    fileReader $scope, $scope.file
      .then (data) ->
        console.log 'UPLOADED', data.length
        ws.emit "serial/#{$scope.tty}/upload", data

# see https://github.com/ghostbar/angular-file-model/blob/master/angular-file-model.js
# fill in the file-model attribute when an upload file has been selected
app.directive 'fileModel', ($parse) -> {
  retrict: 'A'
  link: (scope, elem, attrs) ->
    model = $parse attrs.fileModel
    elem.bind 'change', ->
      scope.$apply ->
        model.assign scope, elem[0].files[0]
}

# see https://github.com/matteosuppo/angular-filereader/blob/master/angular-filereader.js
# return a promise to read a binary file submitted for uploading
app.factory 'fileReader', ($q) ->
  (scope, file) ->
    deferred = $q.defer()

    reader = new FileReader()
    reader.onload = ->
      scope.$apply ->
        deferred.resolve reader.result
    reader.onerror = ->
      scope.$apply ->
        deferred.reject reader.result

    reader.readAsBinaryString file

    deferred.promise