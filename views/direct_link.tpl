<!doctype html>
<html class="no-js" lang="">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <title>Mixer Verifier</title>
        <meta name="description" content="">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <link rel="stylesheet" href="static/css/bootstrap.min.css">
        <link rel="stylesheet" href="static/css/custom.css">
        <style>
            body {
                padding-top: 50px;
                padding-bottom: 20px;
            }
        </style>
        <link rel="stylesheet" href="static/css/bootstrap-theme.min.css">
        <link rel="stylesheet" href="static/css/main.css">

        <script src="static/js/vendor/modernizr-2.8.3-respond-1.4.2.min.js"></script>
    </head>
    <body>
    <nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="/">Home</a>
          <a class="navbar-brand" href="/direct_link">Link Analysis</a>
          <a class="navbar-brand" href="anonymity_set">Anonymity Set</a>
        </div>
      </div>
    </nav>

    <div class="container">
      <form action="/direct_link" method="post">
          <div class="form-group">
            <label>tx_in_hash:<label> 
            <input name="tx_in_hash" class="form-control" type="text" 
            value="490898199a566dcb32a4a9cf45cc7d3cb5f1372e1703c90ad7845acf400f17a5"/>
          </div>
          <div class="form-group">
            <label>tx_out_hash:<label> 
            <input name="tx_out_hash" class="form-control" type="text" 
            value="cb9e8ec8ad02d0edd7b7d9abb85b2312304ffda263493e5ee96e83bc2e78ce17"/>
          </div>
          <div class="form-group">
            <label>user_start_addr:<label> 
            <input name="user_start_addr" class="form-control" type="text" 
            value="1B1tDpsuUBKu25Ktqp8ohziw7qN43FjEQm"/>
          </div>
          <div class="form-group">
            <label>user_end_addr:<label> 
            <input name="user_end_addr" class="form-control" type="text" 
            value="1MV8oVUWVSLTbWDh8p2hof6J7hfnEm4UXM"/>
          </div>
          <div class="form-group">
            <label>mixer_input_addr:<label> 
            <input name="mixer_input_addr" class="form-control" type="text" 
            value="1Luke788hdrUcMqdb2sUdtuzcYqozXgh4L"/>
          </div>
          <input value="Analyze" type="submit" />
      </form>
    </div>

    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
    <script>window.jQuery || document.write('<script src="static/js/vendor/jquery-1.11.2.min.js"><\/script>')</script>
    <script src="static/js/vendor/bootstrap.min.js"></script>
    <script src="static/js/main.js"></script>
    </body>
</html>
