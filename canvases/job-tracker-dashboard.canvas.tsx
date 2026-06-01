import {
  Text,
  H1,
  Stack,
  Row,
  Link,
  Pill,
  useHostTheme,
} from 'cursor/canvas';

interface Job {
  id: string;
  title: string;
  company: string;
  location: string;
  salary: string;
  fitScore: number;
  url: string;
  isNew: boolean;
  isHot: boolean;
}

const JOBS: Job[] = [
  { id: '1', title: 'Senior PM - Fintech', company: 'Razorpay', location: 'Bangalore', salary: '₹35-50 LPA', fitScore: 95, url: 'https://razorpay.com/jobs', isNew: true, isHot: true },
  { id: '2', title: 'PM - Collections CRM', company: 'Paytm', location: 'Noida', salary: '₹38-50 LPA', fitScore: 93, url: 'https://paytm.com/careers', isNew: true, isHot: true },
  { id: '3', title: 'PM - Lending Platform', company: 'Cred', location: 'Bangalore', salary: '₹40-55 LPA', fitScore: 92, url: 'https://cred.club/careers', isNew: true, isHot: true },
  { id: '4', title: 'Product Manager - Payments', company: 'PhonePe', location: 'Bangalore', salary: '₹35-48 LPA', fitScore: 91, url: 'https://phonepe.com/careers', isNew: true, isHot: false },
  { id: '5', title: 'Senior PM - Credit Products', company: 'Slice', location: 'Bangalore', salary: '₹30-45 LPA', fitScore: 90, url: 'https://sliceit.com/careers', isNew: true, isHot: false },
  { id: '6', title: 'PM - Digital Lending', company: 'KreditBee', location: 'Bangalore', salary: '₹28-42 LPA', fitScore: 88, url: 'https://kreditbee.in/careers', isNew: false, isHot: true },
  { id: '7', title: 'Product Lead - Growth', company: 'CRED', location: 'Bangalore', salary: '₹45-60 LPA', fitScore: 87, url: 'https://cred.club/careers', isNew: false, isHot: true },
  { id: '8', title: 'PM - Consumer Finance', company: 'Jupiter', location: 'Mumbai', salary: '₹32-45 LPA', fitScore: 86, url: 'https://jupiter.money/careers', isNew: true, isHot: false },
  { id: '9', title: 'Senior PM - UPI Products', company: 'Google Pay', location: 'Bangalore', salary: '₹50-70 LPA', fitScore: 85, url: 'https://careers.google.com', isNew: false, isHot: true },
  { id: '10', title: 'PM - B2B Payments', company: 'Razorpay', location: 'Bangalore', salary: '₹30-42 LPA', fitScore: 84, url: 'https://razorpay.com/jobs', isNew: false, isHot: false },
  { id: '11', title: 'Product Manager - Wallet', company: 'Amazon Pay', location: 'Bangalore', salary: '₹45-65 LPA', fitScore: 82, url: 'https://amazon.jobs', isNew: false, isHot: false },
  { id: '12', title: 'PM - Credit Risk', company: 'MoneyTap', location: 'Bangalore', salary: '₹25-38 LPA', fitScore: 80, url: 'https://moneytap.com/careers', isNew: true, isHot: false },
  { id: '13', title: 'Senior PM - Insurance Tech', company: 'Policybazaar', location: 'Gurgaon', salary: '₹35-50 LPA', fitScore: 78, url: 'https://policybazaar.com/careers', isNew: false, isHot: false },
  { id: '14', title: 'PM - Merchant Platform', company: 'Paytm', location: 'Noida', salary: '₹30-45 LPA', fitScore: 76, url: 'https://paytm.com/careers', isNew: false, isHot: false },
  { id: '15', title: 'Product Lead - BNPL', company: 'LazyPay', location: 'Mumbai', salary: '₹28-40 LPA', fitScore: 74, url: 'https://lazypay.in/careers', isNew: false, isHot: false },
  { id: '16', title: 'PM - Banking Platform', company: 'Open Financial', location: 'Bangalore', salary: '₹32-45 LPA', fitScore: 72, url: 'https://open.money/careers', isNew: false, isHot: false },
  { id: '17', title: 'Senior PM - Wealth Tech', company: 'Groww', location: 'Bangalore', salary: '₹40-55 LPA', fitScore: 70, url: 'https://groww.in/careers', isNew: true, isHot: false },
  { id: '18', title: 'PM - Stock Trading', company: 'Zerodha', location: 'Bangalore', salary: '₹35-50 LPA', fitScore: 68, url: 'https://zerodha.com/careers', isNew: false, isHot: false },
  { id: '19', title: 'Product Manager - Crypto', company: 'CoinDCX', location: 'Mumbai', salary: '₹30-45 LPA', fitScore: 65, url: 'https://coindcx.com/careers', isNew: false, isHot: false },
  { id: '20', title: 'PM - Investment Platform', company: 'Upstox', location: 'Mumbai', salary: '₹28-42 LPA', fitScore: 62, url: 'https://upstox.com/careers', isNew: false, isHot: false },
  { id: '21', title: 'Senior PM - Tax Tech', company: 'ClearTax', location: 'Bangalore', salary: '₹30-45 LPA', fitScore: 58, url: 'https://cleartax.in/careers', isNew: false, isHot: false },
  { id: '22', title: 'PM - Financial Analytics', company: 'Perfios', location: 'Bangalore', salary: '₹25-38 LPA', fitScore: 55, url: 'https://perfios.com/careers', isNew: false, isHot: false },
];

export default function JobTrackerDashboard() {
  const theme = useHostTheme();
  const perfect = JOBS.filter((j) => j.fitScore >= 90).length;
  const newToday = JOBS.filter((j) => j.isNew).length;

  return (
    <Stack gap={24} style={{ padding: 24, background: theme.bg.editor, minHeight: '100vh' }}>
      <Stack gap={8} style={{ textAlign: 'center' }}>
        <H1>Job Command Centre</H1>
        <Text weight="semibold" style={{ fontSize: 22 }}>
          Abhishek Kumar
        </Text>
        <Text size="small" tone="secondary">
          AI-Powered Job Matching
        </Text>
      </Stack>

      <Row gap={32} justify="center" wrap>
        <Stack gap={4} style={{ textAlign: 'center', minWidth: 80 }}>
          <Text weight="bold" style={{ fontSize: 28, color: theme.accent.primary }}>
            {JOBS.length}
          </Text>
          <Text size="small" tone="secondary">Jobs Found</Text>
        </Stack>
        <Stack gap={4} style={{ textAlign: 'center', minWidth: 80 }}>
          <Text weight="bold" style={{ fontSize: 28, color: theme.accent.primary }}>
            {perfect}
          </Text>
          <Text size="small" tone="secondary">Perfect Match</Text>
        </Stack>
        <Stack gap={4} style={{ textAlign: 'center', minWidth: 80 }}>
          <Text weight="bold" style={{ fontSize: 28 }}>
            {newToday}
          </Text>
          <Text size="small" tone="secondary">New Today</Text>
        </Stack>
      </Row>

      <Text size="small" tone="secondary" style={{ textAlign: 'center' }}>
        For live hosting on your domain, use the web app in /web (see HOSTING.md)
      </Text>

      <Stack gap={8}>
        {JOBS.map((job) => (
          <Row
            key={job.id}
            justify="space-between"
            align="center"
            style={{
              padding: '12px 16px',
              borderRadius: 8,
              border: `1px solid ${theme.stroke.tertiary}`,
              background: theme.bg.secondary,
            }}
          >
            <Stack gap={4} style={{ flex: 1 }}>
              <Row gap={8} align="center" wrap>
                <Text weight="semibold">{job.title}</Text>
                {job.isNew && <Pill tone="warning" size="sm">NEW</Pill>}
                {job.isHot && <Pill tone="warning" size="sm">HOT</Pill>}
              </Row>
              <Row gap={16} wrap>
                <Text size="small">{job.company}</Text>
                <Text size="small" tone="secondary">{job.location}</Text>
                <Text size="small" weight="semibold">{job.salary}</Text>
              </Row>
            </Stack>
            <Row gap={12} align="center">
              <Pill tone={job.fitScore >= 80 ? 'success' : 'warning'} size="md">
                {job.fitScore} FIT
              </Pill>
              <Link href={job.url}>Apply</Link>
            </Row>
          </Row>
        ))}
      </Stack>
    </Stack>
  );
}
