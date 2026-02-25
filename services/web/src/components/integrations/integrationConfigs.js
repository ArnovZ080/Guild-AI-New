import {
    Calendar, DollarSign, FileText, Users, Camera, Globe,
    BarChart, MessageSquare, Zap, Database, Wrench, Shield,
    Mail, Video, Phone, ShoppingCart, Clock
} from 'lucide-react';

/**
 * Integration configurations for the Guild AI platform.
 * Pruned from legacy configurations to focus on core autonomous connectors.
 */

export const integrationConfigs = {
    hubspot: {
        id: 'hubspot',
        name: 'HubSpot',
        category: 'crm',
        status: 'active',
        auth_type: 'oauth',
        icon: Database,
        color: 'bg-orange-500',
        description: 'Connect HubSpot to access CRM data, marketing automation, and sales pipelines. Sync contacts, companies, deals, and tickets seamlessly.',
        capabilities: ['contacts', 'companies', 'deals', 'tickets', 'emails', 'tasks'],
        use_cases: [
            'Auto-enrich contact records from research',
            'Track deal progression and suggest next best actions',
            'Sync marketing campaigns with content strategies',
            'Automate lead follow-ups via AI'
        ],
        setup_complexity: 'medium',
        estimated_setup_time: '2-3 minutes',
        documentation_url: 'https://developers.hubspot.com/',
        api_key_instructions: {
            title: 'How to Get Your HubSpot Access Token',
            steps: [
                {
                    step: 1,
                    action: 'Log in to your HubSpot account',
                    details: 'Go to Settings > Integrations > Private Apps'
                },
                {
                    step: 2,
                    action: 'Create a Private App',
                    details: 'Give it a name like "Guild AI" and select scopes for CRM, Content, and Tickets.'
                },
                {
                    step: 3,
                    action: 'Copy the Access Token',
                    details: 'Copy the generated token and paste it in the field below.'
                }
            ]
        },
        required_permissions: ['crm.objects.contacts.read', 'crm.objects.contacts.write']
    },

    twitter: {
        id: 'twitter',
        name: 'Twitter / X',
        category: 'social_media',
        status: 'active',
        auth_type: 'oauth',
        icon: Globe,
        color: 'bg-blue-400',
        description: 'Automate your social presence. Post content, track engagement, and respond to mentions autonomously.',
        capabilities: ['post_tweet', 'read_mentions', 'search_tweets', 'analytics'],
        use_cases: [
            'Autonomous content distribution',
            'Real-time brand monitoring',
            'AI-driven engagement with industry leaders'
        ],
        setup_complexity: 'easy',
        estimated_setup_time: '5 minutes',
        documentation_url: 'https://developer.twitter.com/',
        api_key_instructions: {
            title: 'Connecting Twitter / X API',
            steps: [
                {
                    step: 1,
                    action: 'Go to Twitter Developer Portal',
                    details: 'Create a new project and app.'
                },
                {
                    step: 2,
                    action: 'Enable User Authentication',
                    details: 'Set up OAuth 2.0 with appropriate permissions.'
                },
                {
                    step: 3,
                    action: 'Copy API Keys',
                    details: 'Generate and copy your Access Token and Secret.'
                }
            ]
        }
    },

    stripe: {
        id: 'stripe',
        name: 'Stripe',
        category: 'payments',
        status: 'active',
        icon: DollarSign,
        color: 'bg-indigo-600',
        description: 'Connect financial data to your AI brain. Analyze revenue, manage subscriptions, and identify billing growth opportunities.',
        capabilities: ['payments', 'customers', 'subscriptions', 'invoices'],
        use_cases: [
            'Real-time revenue monitoring and forecasting',
            'Automatic handling of billing exceptions',
            'Customer churn risk identification'
        ],
        setup_complexity: 'easy',
        estimated_setup_time: '1 minute',
        documentation_url: 'https://stripe.com/docs/api'
    }
};

export const integrationCategories = [
    { id: 'all', name: 'All Services' },
    { id: 'crm', name: 'CRM & Sales', icon: Database },
    { id: 'social_media', name: 'Social Media', icon: Globe },
    { id: 'payments', name: 'Payments & Finance', icon: DollarSign },
    { id: 'communication', name: 'Communication', icon: Mail }
];
