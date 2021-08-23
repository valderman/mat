const today = new Date().getDay();
const friday = today === 5 || window.location.hash === "#friday";
const weekend = [0, 6].includes(today);
const gravity = 0.981;
const blackstoneId = '#blackstone';

let friday_playing = false;

const toggleExpand = element => {
    if (element.classList.contains('clickable')) {
        element.classList.toggle('expand');
    }
};

const playFriday = () => {
    if (!friday_playing) {
        MIDIjs.play('assets/friday.mid');
        friday_playing = true;
        window.setTimeout(() => friday_playing = false, 5*60*1000);
    }
}

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
    const imageNumber = Math.ceil(Math.random()*images);
    return `assets/weekend-${imageNumber}.jpg`;
};

const veggiesToSauce = () => {
    var walker = document.createTreeWalker(
        document.body, 
        NodeFilter.SHOW_TEXT, 
        null
    );

    var node;

    const regexes = [
        /grönsak/i,
        /grönsåss/i
    ];
    while(node = walker.nextNode()) {
        node.nodeValue = regexes.reduce(
            (text, regex) => text.replace(regex, "grönsås"),
            node.nodeValue
        );
    }
};

const frontendMode = () => {
    veggiesToSauce();
    const blackstone = document.querySelector(blackstoneId);
    if (blackstone) {
        blackstone.nextElementSibling.querySelectorAll('li > ul > li').forEach(element => {
            element.innerText += ' samt grönsås';
        });
        blackstone.nextElementSibling.querySelectorAll('section > ul > li').forEach(element => {
            element.firstChild.textContent += ' med grönsås';
        });
    }
};

const onlyBlackstone = () => {
    const blackstone = document.querySelector(blackstoneId);
    if (!blackstone) {
        return;
    }
    blackstone.classList.add('rainbow-text');
    blackstone.classList.add('stupid-animation');
    document.querySelectorAll(`h2:not(${blackstoneId})`).forEach(element => {
        const notBlackstone = document.createTextNode('Inte Blackstone ');
        const tinyName = document.createElement('SUP');
        tinyName.innerText = `(${element.innerText}, som om nån skulle bry sig)`;

        element.innerText = '';
        element.appendChild(notBlackstone);
        element.appendChild(tinyName);
        element.classList.add('not-blackstone');
        element.nextElementSibling.classList.add('not-blackstone');
    });
};

const getModeSetting = () => {
    const valueFromLocalStorage = localStorage.getItem('displaymode');
    return valueFromLocalStorage || document.querySelector('#mode').value;
};

const saveModeSetting = mode => {
    const previousMode = localStorage.getItem('displaymode') || 'normal';
    localStorage.setItem('displaymode', mode);
    document.querySelector('#mode').value = mode;
    return previousMode;
};

const updateDisplayMode = (previousMode, reloadIfNecessary) => {
    const currentMode = getModeSetting();
    switch(currentMode) {
        case 'normal':
            break;
        case 'frontend':
            frontendMode();
            break;
        case 'tobias':
            onlyBlackstone();
            break;
    }
    if (previousMode != currentMode && previousMode != 'normal' && reloadIfNecessary) {
        location.reload();
    }
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

    // Mode select
    document.querySelector('#mode').addEventListener('change', evt => {
        const previousMode = saveModeSetting(evt.target.value);
        updateDisplayMode(previousMode, true);
    });
    const previousMode = saveModeSetting(getModeSetting());
    updateDisplayMode(previousMode, false);
});
