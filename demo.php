<div class="highlight"><pre><span class="go">Python 2.6.1 (r261:67515, Jul  7 2009, 23:51:51) </span>
<span class="go">[GCC 4.2.1 (Apple Inc. build 5646)] on darwin</span>
<span class="go">Type &quot;help&quot;, &quot;copyright&quot;, &quot;credits&quot; or &quot;license&quot; for more information.</span>
<span class="gp">&gt;&gt;&gt; </span><span class="kn">import</span> <span class="nn">idlsave</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">s</span> <span class="o">=</span> <span class="n">idlsave</span><span class="o">.</span><span class="n">read</span><span class="p">(</span><span class="s">&#39;myidlfile.sav&#39;</span><span class="p">)</span>
<span class="go">--------------------------------------------------</span>
<span class="go">Date: Tue Sep 22 11:15:11 2009</span>
<span class="go">User: jdoe</span>
<span class="go">Host: hal9000</span>
<span class="go">--------------------------------------------------</span>
<span class="go">Format: 9</span>
<span class="go">Architecture: x86_64</span>
<span class="go">Operating System: linux</span>
<span class="go">IDL Version: 7.0</span>
<span class="go">--------------------------------------------------</span>
<span class="go">Successfully read 11 records of which:</span>
<span class="go"> - 7 are of type VARIABLE</span>
<span class="go"> - 1 are of type TIMESTAMP</span>
<span class="go"> - 1 are of type NOTICE</span>
<span class="go"> - 1 are of type VERSION</span>
<span class="go">--------------------------------------------------</span>
<span class="go">Available variables:</span>
<span class="go"> - NAN [&lt;type &#39;numpy.ndarray&#39;&gt;]</span>
<span class="go"> - NSTRUCT [&lt;type &#39;dict&#39;&gt;]</span>
<span class="go"> - FLOATARRAY [&lt;type &#39;numpy.ndarray&#39;&gt;]</span>
<span class="go"> - ASTRUCT [&lt;type &#39;dict&#39;&gt;]</span>
<span class="go"> - JOURNALVER [&lt;type &#39;int&#39;&gt;]</span>
<span class="go"> - STRINGARRAY [&lt;type &#39;list&#39;&gt;]</span>
<span class="go"> - ZSTRUCT [&lt;type &#39;dict&#39;&gt;]</span>
<span class="go">--------------------------------------------------</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">s</span><span class="p">(</span><span class="s">&#39;JOURNALVER&#39;</span><span class="p">)</span>
<span class="go">0</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">s</span><span class="p">(</span><span class="s">&#39;FLOATARRAY&#39;</span><span class="p">)</span>
<span class="go">array([[  0.00000000e+00,   1.00000000e+00,   2.00000000e+00, ...,</span>
<span class="go">          9.70000000e+01,   9.80000000e+01,   9.90000000e+01],</span>
<span class="go">       [  1.00000000e+02,   1.01000000e+02,   1.02000000e+02, ...,</span>
<span class="go">          1.97000000e+02,   1.98000000e+02,   1.99000000e+02],</span>
<span class="go">       [  2.00000000e+02,   2.01000000e+02,   2.02000000e+02, ...,</span>
<span class="go">          2.97000000e+02,   2.98000000e+02,   2.99000000e+02],</span>
<span class="go">       ..., </span>
<span class="go">       [  9.70000000e+03,   9.70100000e+03,   9.70200000e+03, ...,</span>
<span class="go">          9.79700000e+03,   9.79800000e+03,   9.79900000e+03],</span>
<span class="go">       [  9.80000000e+03,   9.80100000e+03,   9.80200000e+03, ...,</span>
<span class="go">          9.89700000e+03,   9.89800000e+03,   9.89900000e+03],</span>
<span class="go">       [  9.90000000e+03,   9.90100000e+03,   9.90200000e+03, ...,</span>
<span class="go">          9.99700000e+03,   9.99800000e+03,   9.99900000e+03]], dtype=float32)</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">s</span><span class="p">(</span><span class="s">&#39;NSTRUCT&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">keys</span><span class="p">()</span>
<span class="go">[&#39;COMMENT&#39;, &#39;FLOATARRAY&#39;, &#39;STRINGARRAY&#39;]</span>
</pre></div>
