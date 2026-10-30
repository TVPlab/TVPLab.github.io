"""Bilingual science and creative-world feature for Cherub's lab profile."""
def render_cherub_feature(cn):
    def t(en, zh): return zh if cn else en
    return f'''<section class="cherub-world" aria-labelledby="cherub-world-title">
<div class="cherub-science"><p class="cherub-kicker">CIRCLE OF LIFE · 生之回环</p>
<h2 id="cherub-world-title">Life: Unwired<span>{t('Small cells. Big questions.', '微小的细胞，宏大的问题。')}</span></h2>
<p>{t('My curiosity begins with how cells use energy, and reaches into how we understand life. Circle of Life is my science website: a place to explore metabolism, neuroscience, immunology and bioinnovation beyond a single discipline.', '我的好奇心始于细胞如何利用能量，也延伸至我们如何理解生命。Circle of Life 是我的科学网站：从代谢、神经科学到免疫学与生物创新，跨越学科边界，探索生命。')}</p>
<div class="cherub-topics" aria-label="{t('Topics on Circle of Life', 'Circle of Life 的主题')}"><span>{t('Metabolism', '代谢')}</span><span>{t('Neuroscience', '神经科学')}</span><span>{t('Immunology', '免疫学')}</span></div>
<a class="cherub-primary" href="https://cherubwu.github.io/Circle-of-Life/" target="_blank" rel="noopener">{t('Explore Circle of Life', '探索 Circle of Life')} <span aria-hidden="true">↗</span></a>
</div><aside class="cherub-wonderland"><span class="cherub-spark" aria-hidden="true">✳</span><p class="cherub-kicker">BEYOND THE BENCH</p><h3>{t('A scientist.<br>A storyteller.<br>Always curious.', '科研人。<br>讲故事的人。<br>永远保持好奇。')}</h3><p>{t('Writing, illustration and moments from life outside the lab. A different window into the same curious mind.', '写作、插画，以及实验室之外的生活片段。从另一个窗口，认识同一个好奇的我。')}</p><a href="https://cherubwu.github.io/" target="_blank" rel="noopener">{t('Enter Cherub’s Wonderland', '走进 Cherub 的 Wonderland')} <span aria-hidden="true">↗</span></a></aside>
</section>'''
