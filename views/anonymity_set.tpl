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
          <a class="navbar-brand" href="/direct_link">Direct Link</a>
          <a class="navbar-brand" href="/anonymity_set">Anonymity Set</a>
          <a class="navbar-brand" href="/linkability">Linkability</a>
        </div>
      </div>
    </nav>

    <div class="container padded">
      <form action="/anonymity_set_results" method="post" class="form-horizontal">
          <div class="form-group">
            <label class="col-sm-3">Entering Transaction Hash:</label> 
            <div class="col-sm-9">
              <input name="tx_in_hash" class="form-control" type="text"
              value="664c6c87f005fa8b7314eb5d412e39f0695b17b94fe2882315a3ff0a71f980de" />
              <p class="help-block">The hash of the transaction entering the mixer.</p>
            </div>
          </div>
          <div class="form-group">
            <label class="col-sm-3">Coin Value</label> 
            <div class="col-sm-9">
              <input name="tx_value" class="form-control" type="text" 
              value="1522000"/>
              <p class="help-block">The value, in Satoshis, of the coins you put
              into the mixer.</p>
            </div>
          </div>
          <div class="form-group">
            <label class="col-sm-3">Start Time:</label> 
            <div class="col-sm-9">
              <input name="start_time" class="form-control" type="text" 
              value="0.0"/>
              <p class="help-block">The earliest time after input, in hours, the
              mixing service claimed you would receive your coins.</p>
            </div>
          </div>
          <div class="form-group">
            <label class="col-sm-3">End Time:</label> 
            <div class="col-sm-9">
              <input name="end_time" class="form-control" type="text" 
              value="0.50"/>
              <p class="help-block">The latest time after input, in hours, the
              mixing service claimed you would receive your coins.</p>
            </div>
          </div>
          <div class="form-group">
            <label class="col-sm-3">Flat Fee:</label> 
            <div class="col-sm-9">
              <input name="flat_fee" class="form-control" type="text" 
              value="50000"/>
              <p class="help-block">The flat fee collected by the service.</p>
            </div>
          </div>
          <div class="form-group">
            <label class="col-sm-3">Percent fee, lower bound</label>
            <div class="col-sm-9">
              <input name="percent_fee_lower" class="form-control" type="text" 
              value=".005455"/>
              <p class="help-block">Lower bound, from 0.0 to 1.0, on the percent
              of your coins the service collects.</p>
            </div>
          </div>
          <div class="form-group">
            <label class="col-sm-3">Percent fee, upper bound</label> 
            <div class="col-sm-9">
              <input name="percent_fee_upper" class="form-control" type="text"
              value=".034904"/>
              <p class="help-block">Upper bound, from 0.0 to 1.0, on the percent
              of your coins the service collects.</p>
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
