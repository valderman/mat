const toggleExpand = element => {
    if (element.classList.contains('clickable')) {
        element.classList.toggle('expand');
    }
};

const today = new Date().getDay();
const friday = today === 5 || window.location.hash === "#friday";
const weekend = [0, 6].includes(today);

let friday_playing = false;
const playFriday = () => {
    if (!friday_playing) {
        MIDIjs.play('assets/friday.mid');
        friday_playing = true;
        window.setTimeout(() => friday_playing = false, 5*60*1000);
    }
}

const gravity = 0.981;

const frog = (x, y, xvel, yvel, element) => {
    if (x < 0 ||  x > window.innerWidth || y < -50) {
        document.body.removeChild(element);
        return;
    }

    const renderX = x;
    const renderY = y;
    element.style.left = `${renderX}px`;
    element.style.bottom = `${renderY}px`;

    yvel = yvel - gravity;
    x += xvel;
    y += yvel;
    window.setTimeout(() => frog(x, y, xvel, yvel, element), 10)
};

const launchFrog = () => {
    const element = document.createElement('IMG');
    element.src = 'assets/grodanboll.svg';
    element.style.width = '50px';
    element.style.position = 'fixed';
    const x = Math.random() * window.innerWidth;
    const xvel = (Math.random() * 10 - 5) * 3;
    const yvel = (Math.random() * 5 + 1) * 10;
    if(xvel < 0) {
        element.style.transform = 'scaleX(-1)';
    }
    document.body.appendChild(element);
    frog(x, 1, xvel, yvel, element);
}

const weekendMemeUrl = () => {
    const images = 2;
    const imageNumber = Math.ceil(Math.random()*2);
    return `assets/weekend-${imageNumber}.jpg`;
};

window.addEventListener('DOMContentLoaded', () => {
    if (weekend && !friday) {
        document.body.classList.add('weekend');
        document.querySelector('#weekendmeme').src = weekendMemeUrl();
        return;
    }

    // Expanders for all menu items
    document.querySelectorAll('section > ul > li').forEach(e => {
        if (e.firstElementChild) {
            e.classList.add('clickable');
        }
        e.addEventListener('click', e => toggleExpand(e.target))
    });

    // Friday!
    if (friday) {
        document.body.classList.add('friday');
        document.addEventListener('keydown', e => {
            if(e.code == "KeyF") {
                playFriday();
                launchFrog();
            }
        });
    }
});
