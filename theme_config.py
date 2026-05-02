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
