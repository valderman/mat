const toggleExpand = element => {
    if(element.classList.contains('clickable')) {
        element.classList.toggle('expand');
    }
};

const friday = new Date().getDay() === 5;

const gravity = 9.81;

const frog = (x, y, xvel, yvel, element) => {
    if(x < 0 ||  x > window.innerWidth || y < 0) {
        // Get rid of dead frogs
        return;
    }

    const renderX = x;
    const renderY = y;
    element.style.left = `${renderX}px`;
    element.style.bottom = `${renderY}px`;

    yvel = yvel + gravity;
    x += xvel;
    y += yvel;
    window.setTimeout(() => frog(x, y, xvel, yvel, element), 10)
};

const launchFrog = () => {
    const element = document.createElement('IMG');
    element.src = 'assets/grodanboll.svg';
    element.style.width = '50px';
    element.style.position = 'fixed';
    document.body.appendChild(element);
    frog(100, 1000, 0, -10, element);
}

window.addEventListener('load', () => {
    // Expanders for all menu items
    document.querySelectorAll('section > ul > li').forEach(e => {
        if(e.firstElementChild) {
            e.classList.add('clickable');
        }
        e.addEventListener('click', e => toggleExpand(e.target))
    });

    // Friday!
    if (friday) {
        document.body.classList.add('friday');
        document.addEventListener('keydown', e => {
            if(e.code == "KeyF") {
                console.log("launching frog");
                launchFrog();
            }
        });
    }
});
