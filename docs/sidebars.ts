import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  docsSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Getting Started',
      items: [
        'getting-started/installation',
        'getting-started/quick-start',
        'getting-started/basic-usage',
      ],
    },
    {
      type: 'category',
      label: 'Scripts Reference',
      link: {
        type: 'generated-index',
        title: 'Scripts Reference',
        description: 'Detailed documentation for each analytics script in the repository.',
        slug: '/category/scripts-reference',
      },
      items: [
        'scripts/generate-stats',
        'scripts/generate-stats2',
        'scripts/generate-stats3',
        'scripts/generate-stats4',
        'scripts/generate-stats-fromtemplate',
        'scripts/generate-stats-fromtemplate-withgraphs',
      ],
    },
    {
      type: 'category',
      label: 'Configuration',
      items: [
        'configuration',
        'configuration/timeframes',
        'configuration/blocks',
        'configuration/languages',
        'configuration/graphs',
      ],
    },
    {
      type: 'category',
      label: 'API Reference',
      items: [
        'api/overview',
        'api/git-helpers',
        'api/config-parsing',
        'api/report-generation',
        'api/markdown-processing',
      ],
    },
    'examples',
    'troubleshooting',
    {
      type: 'category',
      label: 'Advanced Topics',
      items: [
        'advanced/github-actions',
        'advanced/custom-templates',
        'advanced/extending-scripts',
      ],
    },
  ],
};

export default sidebars;
