// Мінімалістична статична карта Європи з чорним контуром, без drag/zoom, без підкладки

document.addEventListener('DOMContentLoaded', function() {
    // Створюємо карту, але вимикаємо drag/zoom
    var map = L.map('europe-leaflet-map', {
        zoomControl: false,
        dragging: false,
        scrollWheelZoom: false,
        doubleClickZoom: false,
        boxZoom: false,
        keyboard: false,
        tap: false,
        touchZoom: false,
        attributionControl: false
    }).setView([54, 15], 4);

    // Білий фон
    L.rectangle([[90, -180], [-90, 180]], {color: '#fff', weight: 0, fill: true, fillColor: '#fff', fillOpacity: 1}).addTo(map);

    // Додаємо geoJSON з кордонами країн Європи
    fetch('https://raw.githubusercontent.com/leakyMirror/map-of-europe/master/GeoJSON/europe.geojson')
      .then(response => response.json())
      .then(data => {
        L.geoJSON(data, {
          style: {
            color: '#222',
            weight: 1.5,
            fill: false
          },
          onEachFeature: function (feature, layer) {
            layer.on({
              mouseover: function(e) {
                e.target.setStyle({ color: '#1976d2', weight: 3 });
                if (e.target.bringToFront) e.target.bringToFront();
                const el = e.target._path;
                if (el) el.classList.add('country-highlight');
              },
              mouseout: function(e) {
                e.target.setStyle({ color: '#222', weight: 1.5 });
                const el = e.target._path;
                if (el) el.classList.remove('country-highlight');
              }
            });
            if (feature.properties && feature.properties.NAME) {
              layer.bindTooltip(feature.properties.NAME, {sticky: true, direction: 'top', className: 'country-tooltip'});
            }
          }
        }).addTo(map);
      });
});

// SVG карта: підпис країни при наведенні, анімація виділення площі

document.addEventListener('DOMContentLoaded', function() {
    const countryNames = {
        FR: 'France', DE: 'Germany', ES: 'Spain', IT: 'Italy', PL: 'Poland', UA: 'Ukraine', RO: 'Romania', HU: 'Hungary', CZ: 'Czech Republic', SK: 'Slovakia', AT: 'Austria', GB: 'United Kingdom'
    };
    const tooltip = document.getElementById('svg-tooltip');
    document.querySelectorAll('.country-shape').forEach(function(path) {
        path.addEventListener('mouseenter', function(e) {
            // Виділення країни
            path.classList.add('active');
            // Tooltip
            const id = path.id;
            tooltip.textContent = countryNames[id] || id;
            tooltip.style.display = 'block';
        });
        path.addEventListener('mousemove', function(e) {
            tooltip.style.left = (e.pageX + 12) + 'px';
            tooltip.style.top = (e.pageY - 24) + 'px';
        });
        path.addEventListener('mouseleave', function(e) {
            path.classList.remove('active');
            tooltip.style.display = 'none';
        });
    });
});

// amCharts інтерактивна карта Європи: чорно-білий мінімалізм, без Росії та Svalbard

am5.ready(function() {
    var root = am5.Root.new("amcharts-europe-map");
    root.setThemes([am5themes_Animated.new(root)]);

    var chart = root.container.children.push(
        am5map.MapChart.new(root, {
            panX: "none",
            panY: "none",
            wheelX: "none",
            wheelY: "none",
            projection: am5map.geoMercator(),
            layout: root.verticalLayout
        })
    );

    var polygonSeries = chart.series.push(
        am5map.MapPolygonSeries.new(root, {
            geoJSON: am5geodata_region_world_europeLow,
            exclude: ["RU", "SJ"],
            valueField: "value",
            calculateAggregates: true
        })
    );

    polygonSeries.mapPolygons.template.setAll({
        tooltipText: "{name}",
        interactive: true,
        fill: am5.color(0xFFFFFF),
        stroke: am5.color(0x111111),
        strokeWidth: 1.5
    });

    polygonSeries.mapPolygons.template.states.create("hover", {
        fill: am5.color(0x222222),
        stroke: am5.color(0x111111),
        shadowColor: am5.color(0x111111),
        shadowBlur: 8
    });

    polygonSeries.mapPolygons.template.events.on("pointerover", function(ev) {
        ev.target.toFront();
    });

    // Tooltip стиль
    polygonSeries.mapPolygons.template.adapters.add("tooltipHTML", function(html, target) {
        return '<div style="background:#fff;color:#111;padding:6px 16px;border-radius:6px;border:1px solid #111;font-size:1.1rem;font-weight:500;box-shadow:0 2px 8px #1112;">' + target.dataItem.dataContext.name + '</div>';
    });

    // --- Плавне збільшення країни прямо на карті ---
    let activePolygon = null;
    function resetMapPolygons() {
        polygonSeries.mapPolygons.each(function(polygon) {
            polygon.set("opacity", 1);
            polygon.set("scale", 1);
            polygon.set("zIndex", 0);
        });
        activePolygon = null;
        // Прибрати контент, якщо був
        let info = document.getElementById('country-info-on-map');
        if (info) info.remove();
    }

    polygonSeries.mapPolygons.template.events.on("click", function(ev) {
        // Якщо вже активна — скидаємо
        if (activePolygon === ev.target) {
            resetMapPolygons();
            return;
        }
        resetMapPolygons();
        activePolygon = ev.target;
        // Інші країни — напівпрозорі
        polygonSeries.mapPolygons.each(function(polygon) {
            if (polygon !== activePolygon) polygon.set("opacity", 0.15);
        });
        // Активна країна — збільшуємо, по центру, поверх інших
        activePolygon.set("opacity", 1);
        activePolygon.set("zIndex", 100);
        activePolygon.animate({ key: "scale", to: 6, duration: 500, easing: am5.ease.out(am5.ease.cubic) });
        // Додаємо контент у центр країни (абсолютний div)
        let name = activePolygon.dataItem.dataContext.name;
        let infoDiv = document.createElement('div');
        infoDiv.id = 'country-info-on-map';
        infoDiv.style = 'position:fixed;left:50vw;top:50vh;transform:translate(-50%,-50%) scale(0.7);z-index:9999;color:#fff;font-size:2.2rem;font-weight:600;text-align:center;background:rgba(34,34,34,0.92);padding:32px 48px 24px 48px;border-radius:24px;box-shadow:0 8px 40px #111a;pointer-events:auto;opacity:0;transition:opacity 0.35s, transform 0.35s;';
        infoDiv.innerHTML = `${name}<br><button id='close-country-info' style='margin-top:24px;font-size:1.2rem;padding:8px 32px;border-radius:8px;border:none;background:#fff;color:#222;box-shadow:0 2px 8px #1112;cursor:pointer;'>Закрити</button>`;
        document.body.appendChild(infoDiv);
        setTimeout(() => {
            infoDiv.style.opacity = '1';
            infoDiv.style.transform = 'translate(-50%,-50%) scale(1)';
        }, 10);
        document.getElementById('close-country-info').onclick = resetMapPolygons;
    });

    // Escape скидає виділення
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') resetMapPolygons();
    });

    chart.appear(1000, 100);
}); 