function login(){
    let username = document.getElementById('username').value;
    let pwd = document.getElementById('pwd').value;

    if(!username || !pwd){
        alert('Vui lòng nhập tài khoản và mật khẩu')
    }else {
        let data = {
            "username": username,
            "password": pwd
        }
        fetch('/auth-login-admin', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
        }).then(response => {
            if (response.status === 200){
                alert('success')
                window.location.href = '/admin';
            }else {
                alert('Sai tài khoản hoặc mật khẩu')
            }
        })
    }
}