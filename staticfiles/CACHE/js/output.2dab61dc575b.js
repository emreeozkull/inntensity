let lastScroll=0;const header=document.querySelector('.main-header');window.addEventListener('scroll',()=>{const currentScroll=window.pageYOffset;if(currentScroll<=0){header.classList.remove('scroll-up');return;}
if(currentScroll>lastScroll&&!header.classList.contains('scroll-down')){header.classList.remove('scroll-up');header.classList.add('scroll-down');}else if(currentScroll<lastScroll&&header.classList.contains('scroll-down')){header.classList.remove('scroll-down');header.classList.add('scroll-up');}
lastScroll=currentScroll;});;