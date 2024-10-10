import Document, { Html, Head, Main, NextScript } from 'next/document';
import { ServerStyleSheet } from 'styled-components';

/**
 * MyDocument extends the default Next.js Document to enable server-side rendering
 * of styled-components. This ensures that styles are properly applied on initial load.
 */
export default class MyDocument extends Document {
  /**
   * getInitialProps is used to render pages on the server.
   * Here, we're collecting styles from styled-components.
   * 
   * @param {Object} ctx - The context object
   * @returns {Object} The initial props with collected styles
   */
  static async getInitialProps(ctx) {
    const sheet = new ServerStyleSheet();
    const originalRenderPage = ctx.renderPage;

    try {
      // Wrap the app with the ServerStyleSheet to collect styles
      ctx.renderPage = () =>
        originalRenderPage({
          enhanceApp: (App) => (props) =>
            sheet.collectStyles(<App {...props} />),
        });

      // Run the parent getInitialProps
      const initialProps = await Document.getInitialProps(ctx);
      
      // Return the props with collected styles
      return {
        ...initialProps,
        styles: (
          <>
            {initialProps.styles}
            {sheet.getStyleElement()}
          </>
        ),
      };
    } finally {
      sheet.seal();
    }
  }

  /**
   * Render method defines the structure of the document
   * 
   * @returns {JSX.Element} The document structure
   */
  render() {
    return (
      <Html lang="en">
        <Head />
        <body>
          <Main />
          <NextScript />
        </body>
      </Html>
    );
  }
}