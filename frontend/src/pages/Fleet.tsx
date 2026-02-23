import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { Ship } from "lucide-react";

const vessels = [
  { name: "MV Oceanic Star", status: "En Route", fuel: "87%", eta: "14h 22m" },
  { name: "MV Green Horizon", status: "Optimizing", fuel: "62%", eta: "8h 05m" },
  { name: "MV Pacific Breeze", status: "Docked", fuel: "95%", eta: "—" },
  { name: "MV Coral Voyager", status: "En Route", fuel: "74%", eta: "22h 40m" },
];

const statusColor: Record<string, string> = {
  "En Route": "bg-primary",
  Optimizing: "bg-amber-400",
  Docked: "bg-muted-foreground",
};

const Fleet = () => {
  return (
    <div className="min-h-screen ocean-gradient flex flex-col">
      <Navbar />
      <main className="flex-1 pt-20">
        <section className="px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto pt-8 pb-4">
          <h1 className="text-2xl sm:text-3xl font-bold text-foreground mb-1">Fleet</h1>
          <p className="text-sm text-muted-foreground">Active vessel tracking</p>
        </section>

        <section className="py-8 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
          <div className="grid gap-4">
            {vessels.map((v, i) => (
              <div
                key={v.name}
                className="glass-card-hover p-5 flex items-center justify-between"
                style={{ animation: `slideUp 0.5s ease-out ${i * 80}ms both` }}
              >
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center">
                    <Ship className="w-5 h-5 text-primary" />
                  </div>
                  <div>
                    <span className="text-sm font-semibold text-foreground">{v.name}</span>
                    <div className="flex items-center gap-1.5 mt-0.5">
                      <span className={`w-2 h-2 rounded-full ${statusColor[v.status] ?? "bg-muted-foreground"}`} />
                      <span className="text-xs text-muted-foreground">{v.status}</span>
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-8 text-right">
                  <div>
                    <span className="text-xs text-muted-foreground block">Fuel</span>
                    <span className="text-sm font-semibold text-foreground">{v.fuel}</span>
                  </div>
                  <div>
                    <span className="text-xs text-muted-foreground block">ETA</span>
                    <span className="text-sm font-semibold text-foreground">{v.eta}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>
      </main>
      <Footer />
    </div>
  );
};

export default Fleet;
