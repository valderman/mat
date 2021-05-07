const toggleExpand = element => {
    if(element.classList.contains('clickable')) {
        element.classList.toggle('expand');
    }
};

const friday = new Date().getDay() === 5;

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
    }
});
