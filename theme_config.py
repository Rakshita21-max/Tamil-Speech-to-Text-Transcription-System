custom_css = """
.theme-switch-wrapper {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding: 10px;
}
.theme-switch {
  position: relative;
  display: inline-block;
  width: 140px;
  height: 50px;
}
.theme-switch input { 
  opacity: 0;
  width: 0;
  height: 0;
}
.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #e6e9ef;
  transition: .4s;
  border-radius: 50px;
  box-shadow: inset 5px 5px 10px #c8cdd4, inset -5px -5px 10px #ffffff;
  display: flex;
  align-items: center;
  overflow: hidden;
}
.mode-text {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  font-weight: 700;
  font-size: 13px;
  position: absolute;
  z-index: 1;
  transition: .4s;
}
.light-text {
  right: 15px;
  color: #929aab;
}
.dark-text {
  left: 15px;
  color: #8b92a5;
  opacity: 0;
}
.icon-container {
  position: absolute;
  height: 40px;
  width: 40px;
  left: 5px;
  bottom: 5px;
  background-color: #f0f3f8;
  border-radius: 50%;
  transition: .4s;
  box-shadow: 4px 4px 8px #c8cdd4, -4px -4px 8px #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2;
  color: #929aab;
}
.moon-icon {
  display: none;
}
/* Dark Mode Styles triggered by the checkbox */
input:checked + .slider {
  background-color: #2a2d3c;
  box-shadow: inset 5px 5px 10px #1e202a, inset -5px -5px 10px #363a4e;
}
input:checked + .slider .light-text {
  opacity: 0;
}
input:checked + .slider .dark-text {
  opacity: 1;
  color: #8b92a5;
}
input:checked + .slider .icon-container {
  transform: translateX(90px);
  background-color: #7b819f; 
  box-shadow: 4px 4px 8px #1e202a, -4px -4px 8px #363a4e;
  color: #ffffff; 
}
input:checked + .slider .sun-icon {
  display: none;
}
input:checked + .slider .moon-icon {
  display: block;
}
"""

html_switch = """
<div class="theme-switch-wrapper">
  <label class="theme-switch" for="theme-checkbox">
    <input type="checkbox" id="theme-checkbox" onchange="
      var isDark = this.checked;
      var html = document.documentElement;
      var body = document.body;
      var app = document.querySelector('gradio-app');
      
      if (isDark) {
         body.classList.add('dark');
         html.classList.add('dark');
         if(app) app.classList.add('dark');
      } else {
         body.classList.remove('dark');
         html.classList.remove('dark');
         if(app) app.classList.remove('dark');
      }
    " />
    <div class="slider round">
      <span class="mode-text light-text">LIGHT MODE</span>
      <span class="mode-text dark-text">DARK MODE</span>
      <div class="icon-container">
        <!-- Sun Icon -->
        <svg class="sun-icon" viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="5"></circle>
          <line x1="12" y1="1" x2="12" y2="3"></line>
          <line x1="12" y1="21" x2="12" y2="23"></line>
          <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
          <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
          <line x1="1" y1="12" x2="3" y2="12"></line>
          <line x1="21" y1="12" x2="23" y2="12"></line>
          <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
          <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
        </svg>
        <!-- Moon Icon -->
        <svg class="moon-icon" viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
        </svg>
      </div>
    </div>
  </label>
</div>
<script>
  setTimeout(function() {
      var isDark = document.body.classList.contains('dark') || 
                   document.documentElement.classList.contains('dark') || 
                   (document.querySelector('gradio-app') && document.querySelector('gradio-app').classList.contains('dark'));
      var cb = document.getElementById('theme-checkbox');
      if(cb && isDark) { cb.checked = true; }
  }, 500);
</script>
"""
