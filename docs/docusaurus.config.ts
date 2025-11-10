import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'Repository Analytics Documentation',
  tagline: 'Comprehensive guide to automated repository statistics generation',
  favicon: 'img/favicon.ico',

  future: {
    v4: true,
  },

  url: 'https://your-domain.com',
  baseUrl: '/',

  organizationName: 'your-org',
  projectName: 'analrepo',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          routeBasePath: '/docs',
          sidebarPath: './sidebars.ts',
          editUrl: 'https://github.com/your-org/analrepo/tree/main/docs/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: 'img/docusaurus-social-card.jpg',
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'Repo Analytics',
      logo: {
        alt: 'Repository Analytics Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'docsSidebar',
          position: 'left',
          label: 'Documentation',
        },
        {
          href: 'https://github.com/your-org/analrepo',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Documentation',
          items: [
            {
              label: 'Getting Started',
              to: '/docs/intro',
            },
            {
              label: 'Scripts Reference',
              to: '/docs/category/scripts-reference',
            },
            {
              label: 'Configuration',
              to: '/docs/configuration',
            },
          ],
        },
        {
          title: 'Resources',
          items: [
            {
              label: 'API Reference',
              to: '/docs/api/overview',
            },
            {
              label: 'Examples',
              to: '/docs/examples',
            },
            {
              label: 'Troubleshooting',
              to: '/docs/troubleshooting',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/your-org/analrepo',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Repository Analytics Project. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['python', 'bash', 'json', 'yaml'],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
