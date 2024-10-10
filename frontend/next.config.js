const withTM = require('next-transpile-modules')(['tone']);

module.exports = withTM({
  reactStrictMode: false,
  compiler: {
    styledComponents: true,
  },
});