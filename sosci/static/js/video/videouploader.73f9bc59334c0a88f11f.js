(function webpackUniversalModuleDefinition(root, factory) {
	if(typeof exports === 'object' && typeof module === 'object')
		module.exports = factory();
	else if(typeof define === 'function' && define.amd)
		define([], factory);
	else {
		var a = factory();
		for(var i in a) (typeof exports === 'object' ? exports : root)[i] = a[i];
	}
})(window, function() {
return /******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "js";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = "./src/videouploader/index.js");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./src/videouploader/index.js":
/*!************************************!*\
  !*** ./src/videouploader/index.js ***!
  \************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";
eval("\n\nfunction _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError(\"Cannot call a class as a function\"); } }\n\nfunction _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if (\"value\" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }\n\nfunction _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }\n\nvar VideoUploader =\n/*#__PURE__*/\nfunction () {\n  function VideoUploader(upload_url, csrf_token) {\n    var _this = this;\n\n    _classCallCheck(this, VideoUploader);\n\n    this.upload_url = upload_url;\n    this.csrf_token = csrf_token;\n    this.upload = null;\n    this.uploadIsRunning = false;\n    this.toggleBtn = document.querySelector(\"#toggle-btn\");\n    this.resumeCheckbox = document.querySelector(\"#resume\");\n    this.video_file_input = window.$(\"input[name=video_file]\");\n    this.progressBar = document.querySelector(\".progress-bar\");\n    this.alertBox = document.querySelector(\"#support-alert\");\n    this.uploadList = document.querySelector(\"#upload-list\");\n    this.endpointInput = document.querySelector(\"#endpoint\");\n\n    if (!window.tus.isSupported) {\n      alertBox.classList.remove(\"hidden\");\n    }\n\n    if (!this.toggleBtn) {\n      throw new Error(\"Toggle button not found on this page. Aborting upload-demo. \");\n    }\n\n    this.toggleBtn.addEventListener(\"click\", function (e) {\n      e.preventDefault();\n\n      _this.create_video();\n    });\n  }\n\n  _createClass(VideoUploader, [{\n    key: \"create_video\",\n    value: function create_video() {\n      var _this2 = this;\n\n      var file = this.video_file_input.prop(\"files\")[0];\n      var course_module_form_data = {};\n      window.$(\"#course-module-form\").serializeArray().forEach(function (x) {\n        course_module_form_data[x.name] = x.value;\n      });\n      window.$.ajax({\n        url: this.upload_url,\n        method: \"POST\",\n        dataType: \"json\",\n        data: {\n          name: course_module_form_data.name,\n          duration: course_module_form_data.duration,\n          file_size: file.size,\n          csrfmiddlewaretoken: this.csrf_token\n        }\n      }).done(function (data, textStatus, jqXHR) {\n        if (_this2.upload) {\n          if (_this2.uploadIsRunning) {\n            _this2.upload.abort();\n\n            _this2.toggleBtn.textContent = \"resume upload\";\n            _this2.uploadIsRunning = false;\n          } else {\n            _this2.upload.start();\n\n            _this2.toggleBtn.textContent = \"pause upload\";\n            _this2.uploadIsRunning = true;\n          }\n        } else {\n          if (_this2.video_file_input.prop(\"files\").length > 0) {\n            _this2.start_upload(data.upload.upload_link);\n          } else {\n            _this2.video_file_input.click();\n          }\n        }\n      });\n    }\n  }, {\n    key: \"start_upload\",\n    value: function start_upload(upload_link) {\n      var _this3 = this;\n\n      var file = this.video_file_input.prop(\"files\")[0]; // Only continue if a file has actually been selected.\n      // IE will trigger a change event even if we reset the input element\n      // using reset() and we do not want to blow up later.\n\n      if (!file) {\n        return;\n      }\n\n      var chunkSize = 100 * 1024 * 1024;\n      this.toggleBtn.textContent = \"pause upload\";\n      var options = {\n        endpoint: upload_link,\n        uploadUrl: upload_link,\n        resume: true,\n        uploadSize: file.size,\n        chunkSize: chunkSize,\n        retryDelays: [0, 1000, 3000, 5000],\n        metadata: {\n          filename: file.name,\n          filetype: file.type\n        },\n        onError: function onError(error) {\n          if (error.originalRequest) {\n            if (window.confirm(\"Failed because: \" + error + \"\\nDo you want to retry?\")) {\n              _this3.upload.start();\n\n              _this3.uploadIsRunning = true;\n              return;\n            }\n          } else {\n            window.alert(\"Failed because: \" + error);\n          }\n\n          _this3.reset();\n        },\n        onProgress: function onProgress(bytesUploaded, bytesTotal) {\n          var percentage = (bytesUploaded / bytesTotal * 100).toFixed(2);\n          _this3.progressBar.style.width = percentage + \"%\";\n          console.log(bytesUploaded, bytesTotal, percentage + \"%\");\n        },\n        onSuccess: function onSuccess() {\n          var anchor = document.createElement(\"a\");\n          anchor.textContent = \"Download \" + _this3.upload.file.name + \" (\" + _this3.upload.file.size + \" bytes)\";\n          anchor.href = _this3.upload.url;\n          anchor.className = \"btn btn-success\";\n\n          _this3.uploadList.appendChild(anchor);\n\n          _this3.reset();\n\n          location.reload();\n        }\n      };\n      this.upload = new tus.Upload(file, options);\n      this.upload.start();\n      this.uploadIsRunning = true;\n    }\n  }, {\n    key: \"reset\",\n    value: function reset() {\n      this.video_file_input.value = \"\";\n      this.toggleBtn.textContent = \"start upload\";\n      this.upload = null;\n      this.uploadIsRunning = false;\n    }\n  }]);\n\n  return VideoUploader;\n}();\n\nwindow.VideoUploader = VideoUploader;\n\n//# sourceURL=webpack:///./src/videouploader/index.js?");

/***/ })

/******/ });
});