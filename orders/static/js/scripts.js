document.addEventListener('DOMContentLoaded', () => {
    x = document.querySelector('#mail');
    x.addEventListener('keyup', () => {
        if (x.value.length > 64) {
            alert("Max value exceeded!")
            document.querySelector('#regBtn').disabled = true;
        } else
            document.querySelector('#regBtn').disabled = false;
    });
    y = document.querySelector('#cpass');
    y.addEventListener('keyup', () => {
        pwd = document.querySelector('#mpass').value;
        if (pwd == y.value) {
            document.querySelector('#regBtn').disabled = false;
            y.style.borderColor = '#ced4da'
        } else {
            document.querySelector('#regBtn').disabled = true;
            y.style.borderColor = 'red';
        }
    });

    z = document.querySelector('#mpass');
    z.addEventListener('keyup', () => {
        y.value = "";
    });

    
});
