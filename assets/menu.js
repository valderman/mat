const toggleExpand = element => {
    if(element.classList.contains('clickable')) {
        element.classList.toggle('expand');
    }
};

window.addEventListener('load', () => {
    const sublists = document.querySelectorAll('main > ul > li');
    sublists.forEach(e => {
        if(e.firstElementChild) {
            e.classList.add('clickable');
        }
        e.addEventListener('click', e => toggleExpand(e.target))
    });
});
