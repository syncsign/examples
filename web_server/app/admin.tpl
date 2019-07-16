<nav aria-label="breadcrumb">
  <ol class="breadcrumb">
    <li class="breadcrumb-item"><a href="/">Home</a></li>
    <li class="breadcrumb-item active" aria-current="page">Admin</li>
  </ol>
</nav>
<h1>Admin Setup</h1>
<form action='/admin' method='POST'>
  <div class="form-group">
    <label for="passwd">Set a password</label>
    <input type="password" name="passwd" id="passwd" class="form-control" placeholder="Enter a password here" value="{passwd}">
  </div>
  <button type="submit" class="btn btn-primary">Submit</button>
</form>
