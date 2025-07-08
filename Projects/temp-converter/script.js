function temp(event) {
    const currentval = +event.target.value;
    let c, f, k;

    switch (event.target.name) {
        case 'ce':
            c = currentval.toFixed(2);
            f = (currentval * 1.8 + 32).toFixed(2);
            k = (currentval + 273.32).toFixed(2);
            break;
        case 'far':
            c = ((currentval - 32) / 1.8).toFixed(2);
            f = currentval.toFixed(2);
            k = (((currentval - 32) / 1.8) + 273.32).toFixed(2);
            break;
        case 'ke':
            c = (currentval - 273.32).toFixed(2);
            f = (((currentval - 273.32) * 1.8) + 32).toFixed(2);
            k = currentval.toFixed(2);
            break;
        default:
            return;
    }

    
    document.getElementById("ce").value = c;
    document.getElementById("far").value = f;
    document.getElementById("ke").value = k;
}
