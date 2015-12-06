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

    <div class="container padded">
      <form action="/anonymity_set_results" method="post" class="form-horizontal">
          <div class="form-group">
            <label class="col-sm-3">tx_in_hash:</label> 
            <div class="col-sm-9">
              <input name="tx_in_hash" class="form-control" type="text"
              value="0197dabc3c31c8221b5d7883a9d03240bcf7a3042e1bf6dcc26c8d3aa60c58ab" />
            </div>
          </div>
          <div class="form-group">
            <label class="col-sm-3">tx_value (in satoshis):</label> 
            <div class="col-sm-9">
              <input name="tx_value" class="form-control" type="text" 
              value="1523000"/>
            </div>
          </div>
          <div class="form-group">
            <label class="col-sm-3">start_time (in hours):</label> 
            <div class="col-sm-9">
              <input name="start_time" class="form-control" type="text" 
              value="0.0"/>
            </div>
          </div>
          <div class="form-group">
            <label class="col-sm-3">end_time (in hours):</label> 
            <div class="col-sm-9">
              <input name="end_time" class="form-control" type="text" 
              value="0.75"/>
            </div>
          </div>
          <div class="form-group">
            <label class="col-sm-3">Flat Fee (in Satoshis):</label> 
            <div class="col-sm-9">
              <input name="flat_fee" class="form-control" type="text" 
              value="50000"/>
            </div>
          </div>
          <div class="form-group">
            <label class="col-sm-3">percent_fee_lower (from 0.0 to 1.0):</label> 
            <div class="col-sm-9">
              <input name="percent_fee_lower" class="form-control" type="text" 
              value=".005"/>
            </div>
          </div>
          <div class="form-group">
            <label class="col-sm-3">percent_fee_upper (from 0.0 to 1.0):</label> 
            <div class="col-sm-9">
              <input name="percent_fee_upper" class="form-control" type="text"
              value=".006"/>
            </div>
          </div>
          <input value="Analyze" class="col-sm-offset-3 col-sm-9 btn btn-default" type="submit" />
      </form>
    </div>

    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
    <script>window.jQuery || document.write('<script src="static/js/vendor/jquery-1.11.2.min.js"><\/script>')</script>
    <script src="static/js/vendor/bootstrap.min.js"></script>
    <script src="static/js/main.js"></script>
    </body>
</html>
