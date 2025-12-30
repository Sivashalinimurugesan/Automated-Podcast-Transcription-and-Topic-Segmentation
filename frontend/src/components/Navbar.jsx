export default function Features() {
  const features = [
    { title: "Lightning Fast Transcription"},
    { title: "Intelligent Topic Segmentation"  },
    { title: "Smart Search & Navigation" },
    { title: "AI-Generated Summaries"},
  ];

  return (
    <section className="mt-24 px-12">
      <h2 className="text-center font-semibold">Powerful Features</h2>

      <div className="grid md:grid-cols-4 gap-6 mt-10">
        {features.map((f, i) => (
          <div
            key={i}
            className="bg-white rounded-2xl p-6 shadow hover:shadow-lg transition"
          >
            <div className="text-2xl">{f.icon}</div>
            <h3 className="mt-4 font-medium">{f.title}</h3>
            <p className="text-sm text-gray-500 mt-2">
              Advanced AI powered processing.
            </p>
          </div>
        ))}
      </div>
    </section>
  );
}
