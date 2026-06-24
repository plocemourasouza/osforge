# Chart Types — UI Design Intelligence

25 tipos de chart para dashboards e analytics. Para cada um: quando usar, quando NÃO usar, biblioteca e acessibilidade.

---

### Line Chart — Trend Over Time
**Usar quando:** Data has a time axis; user needs to observe rise/fall trends or rate of change over a continuous period  
**Não usar:** Fewer than 4 data points (use stat card); more than 6 series (visual noise); no time dimension exists  
**Bibliotecas:** Chart.js, Recharts, ApexCharts  
**A11y:** Differentiate series by line style (solid/dashed/dotted) not color alone. Add pattern overlays for colorblind users.

### Bar Chart (Horizontal or Vertical) — Compare Categories
**Usar quando:** Comparing discrete categories by magnitude; ranking or ordering is the core insight; categories ≤ 15  
**Não usar:** Categories > 15 (use table or search); data has time dimension (use line); showing proportions (use waffle/stacked)  
**Bibliotecas:** Chart.js, Recharts, D3.js  
**A11y:** Value labels on each bar by default. Sort control for user reordering.

### Pie Chart or Donut — Part-to-Whole
**Usar quando:** ≤5 categories; one dominant segment vs rest; emphasis on visual proportion over exact values  
**Não usar:** Categories > 5; slice differences < 5% (visually indistinguishable); user needs precise values; accessibility-first context  
**Bibliotecas:** Chart.js, Recharts, D3.js  
**A11y:** Pie charts fail WCAG for colorblind users. Slices rely on color alone. Avoid as primary chart in a11y contexts.

### Scatter Plot or Bubble Chart — Correlation / Distribution
**Usar quando:** Exploring relationship between two continuous variables; identifying clusters or outliers in a dataset  
**Não usar:** Variables are categorical (use grouped bar); fewer than 20 points (patterns aren't meaningful); mobile-primary context  
**Bibliotecas:** D3.js, Plotly, Recharts  
**A11y:** Provide data table alternative. Combine color + shape distinction for colorblind users.

### Heat Map or Choropleth — Heatmap / Intensity
**Usar quando:** Showing intensity/density across a 2D grid; time-based patterns (e.g., activity by hour × day)  
**Não usar:** Fewer than 20 cells (use bar); user needs to read exact values; colorblind users without pattern fallback  
**Bibliotecas:** D3.js, Plotly, ApexCharts  
**A11y:** Pattern overlay for colorblind users. Numerical value on hover. Legend must include scale ticks.

### Choropleth Map or Bubble Map — Geographic Data
**Usar quando:** Data has a regional/location dimension; spatial distribution is the core insight for the user  
**Não usar:** Regions have very different sizes making visual comparison misleading (use bar); mobile-primary context  
**Bibliotecas:** D3.js, Mapbox, Leaflet  
**A11y:** Include text labels for major regions. Provide keyboard navigation between regions.

### Funnel Chart or Sankey — Funnel / Flow
**Usar quando:** Sequential multi-stage process; showing conversion or drop-off rates between defined stages  
**Não usar:** Stages aren't sequential; values don't decrease monotonically (use bar); fewer than 3 stages  
**Bibliotecas:** D3.js, Recharts, Custom SVG  
**A11y:** Explicit conversion % as text per stage. Stage labels always visible. Linear list view as fallback.

### Gauge Chart or Bullet Chart — Performance vs Target
**Usar quando:** Single KPI measured against a defined target or threshold; dashboard summary context  
**Não usar:** No target or benchmark exists; comparing multiple KPIs at once (use bullet chart grid)  
**Bibliotecas:** D3.js, ApexCharts, Custom SVG  
**A11y:** Always show numerical value + % of target as text beside chart. Never rely on color position alone.

### Line with Confidence Band — Time-Series Forecast
**Usar quando:** Historical data + model predictions; communicating uncertainty range to non-technical stakeholders  
**Não usar:** No historical baseline; prediction confidence is too low to be useful; audience is not data-literate  
**Bibliotecas:** Chart.js, ApexCharts, Plotly  
**A11y:** Toggle between actual-only and forecast views. Legend must distinguish lines beyond color (solid vs dashed).

### Line Chart with Highlights — Anomaly Detection
**Usar quando:** Monitoring a time-series for outliers; alerting users to unexpected spikes or dips in operational data  
**Não usar:** Anomalies are predefined categories (use bar with highlight); real-time context without a pause control  
**Bibliotecas:** D3.js, Plotly, ApexCharts  
**A11y:** Use shape marker (not color only) for anomaly points. Add text annotation per anomaly event.

### Treemap — Hierarchical / Nested Data
**Usar quando:** Showing size relationships within a hierarchy; overview of proportional structure (e.g., budget breakdown)  
**Não usar:** Hierarchy depth > 3 levels (too complex to read); user needs to compare sibling values precisely  
**Bibliotecas:** D3.js, Recharts, ApexCharts  
**A11y:** Poor baseline accessibility. Always provide table alternative as primary view. Label all large areas.

### Sankey Diagram — Flow / Process Data
**Usar quando:** Showing how quantities flow between nodes; multi-source multi-target distribution  
**Não usar:** Flow directions form loops (use network graph); fewer than 3 source-target pairs; mobile-primary context  
**Bibliotecas:** D3.js (d3-sankey), Plotly  
**A11y:** Structural flow charts cannot be conveyed by color alone. Provide flow table. Avoid on mobile.

### Waterfall Chart — Cumulative Changes
**Usar quando:** Showing how individual positive/negative components add up to a final total (e.g., P&L, budget variance)  
**Não usar:** Changes are not additive; more than 12 bars (readability breaks); audience expects a simple total  
**Bibliotecas:** ApexCharts, Highcharts, Plotly  
**A11y:** Color + directional arrow icon per bar (not color alone). Labels on every bar.

### Radar / Spider Chart — Multi-Variable Comparison
**Usar quando:** Comparing multiple entities across the same fixed set of attributes (e.g., product feature comparison)  
**Não usar:** Axes > 8 (unreadable); values need precise comparison (use grouped bar); audience unfamiliar with radar charts  
**Bibliotecas:** Chart.js, Recharts, ApexCharts  
**A11y:** Limit axes to 5–8. Always provide grouped bar chart alternative for precise reading.

### Candlestick Chart — Stock / Trading OHLC
**Usar quando:** Financial time-series with Open/High/Low/Close data; trading or investment product context only  
**Não usar:** Non-financial audience; no OHLC data available (use line chart); accessibility-first context  
**Bibliotecas:** Lightweight Charts (TradingView), ApexCharts  
**A11y:** Provide OHLC data table. Colorblind: use fill vs outline pattern (bullish = filled, bearish = hollow).

### Network Graph — Relationship / Connection Data
**Usar quando:** Mapping connections between entities; network topology or social graph exploration context  
**Não usar:** Node count > 500 without clustering pre-applied; user needs precise connection counts; mobile context  
**Bibliotecas:** D3.js (d3-force), Vis.js, Cytoscape.js  
**A11y:** Fundamentally inaccessible without alternative. Never use as sole representation. Always provide list alternative.

### Box Plot — Distribution / Statistical
**Usar quando:** Showing spread, median, and outliers of a dataset; comparing distributions across multiple groups  
**Não usar:** Fewer than 20 data points per group (distribution is not meaningful); audience unfamiliar with statistical charts  
**Bibliotecas:** Plotly, D3.js, Chart.js (plugin)  
**A11y:** Include stats summary table. Annotate outlier count in chart subtitle.

### Bullet Chart — Performance vs Target (Compact)
**Usar quando:** Dashboard with multiple KPIs side by side; space-constrained contexts where a gauge is too large  
**Não usar:** Single KPI with emphasis (use gauge); data has no defined target range; fewer than 3 KPIs  
**Bibliotecas:** D3.js, Plotly, Custom SVG  
**A11y:** All values always visible as text. Color ranges are labeled with text thresholds not color alone.

### Waffle Chart — Proportional / Percentage
**Usar quando:** Showing what fraction of a whole is filled; percentage progress in a visually engaging and accessible format  
**Não usar:** More than 5 categories (use stacked bar); exact values matter over visual proportion; very tight space  
**Bibliotecas:** D3.js, React-Waffle, Custom CSS Grid  
**A11y:** Better than pie for accessibility. Percentage text label always visible. Each cell has aria-label.

### Sunburst Chart — Hierarchical Proportional
**Usar quando:** Exploring nested proportions where both hierarchy and relative size matter (e.g., org spend breakdown)  
**Não usar:** More than 3 hierarchy levels (outer rings become unreadable); precision matters over overview; mobile  
**Bibliotecas:** D3.js (d3-hierarchy), Recharts, ApexCharts  
**A11y:** Poor accessibility beyond 2 levels. Mandatory table alternative required for any production use.

### Decomposition Tree — Root Cause Analysis
**Usar quando:** Decomposing a metric into contributing factors; AI-assisted analysis or BI drill-down scenarios  
**Não usar:** No clear parent-child causal relationship; audience expects a summary rather than exploration  
**Bibliotecas:** Power BI (native), React-Flow, Custom D3.js  
**A11y:** Keyboard-navigable expand/collapse. Screen reader announces node value and % contribution.

### 3D Scatter / Surface Plot — 3D Spatial Data
**Usar quando:** Scientific/engineering context where Z-axis carries essential info not expressible in 2D  
**Não usar:** 2D projection conveys the same insight; mobile context; accessibility-required environments; standard business dashboards  
**Bibliotecas:** Three.js, Deck.gl, Plotly 3D  
**A11y:** 3D spatial charts are fundamentally inaccessible. Must not be used as primary chart type in any product UI.

### Streaming Area Chart — Real-Time Streaming
**Usar quando:** Live monitoring dashboards; IoT/ops data updating at ≥1 Hz; user needs current value at a glance  
**Não usar:** Update frequency < 1/min (use periodic-refresh line chart); flashing content without reduced-motion support  
**Bibliotecas:** Smoothed D3.js, CanvasJS  
**A11y:** Pause/resume control required. Current value as large visible text KPI. Respect prefers-reduced-motion.

### Word Cloud with Sentiment — Sentiment / Emotion
**Usar quando:** NLP output visualization; exploratory analysis of text corpus sentiment; frequency-weighted keyword overview  
**Não usar:** Precise values matter (word size is inherently imprecise); screen-reader context; corpus < 50 items  
**Bibliotecas:** D3-cloud, Highcharts, Nivo  
**A11y:** Word clouds fail screen readers. Never use as sole output of NLP analysis. Always pair with list view.

### Process Map / Graph — Process Mining
**Usar quando:** Analyzing event logs to visualize actual process flows; identifying bottlenecks and deviations in ops/product funnels  
**Não usar:** No event log data available; audience expects a static flowchart (use diagram tool); node count > 100 without pre-filtering  
**Bibliotecas:** React-Flow, Cytoscape.js, Recharts  
**A11y:** Complex graphs are hard to navigate. Provide path summary text. Highlight top 3 bottlenecks as annotations.
