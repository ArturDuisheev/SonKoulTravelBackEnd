import React from "react";
import Warning from "../ui/Warning";
import Accordeon from "../ui/Accordeon";
import { useSelector } from "react-redux";
import { RootState } from "../../store/store";
import useMatchMedia from "use-match-media";
import geoIcon from "../../assets/images/tour/geo-icon.svg";
import car from "../../assets/images/tour/car.svg";
import food from "../../assets/images/tour/food.svg";
import horse from "../../assets/images/tour/horse.svg";
import byfoot from "../../assets/images/tour/byfoot.svg";
import sleep from "../../assets/images/tour/sleep.svg";
import road from "../../assets/images/tour/road.svg";

const Program: React.FC = () => {
  const { data } = useSelector((state: RootState) => state.tour);
  const isTb = useMatchMedia("(max-width: 768px)");

  const getIconLocation = (type: string) => {
    switch (type) {
      case "1":
        return geoIcon;
      case "2":
        return food;
      case "3":
        return sleep;
      default:
        break;
    }
  };

  const getIconMoving = (type: string) => {
    switch (type) {
      case "На машине":
      case "car":
        return car;
      case "Верхом":
      case "horse":
        return horse;
      case "Пешком":
      case "on foot":
        return byfoot;
      default:
        break;
    }
  };

  if (!data.program.length) return <></>;

  return (
    <section className="pl-10 pb-20 bottom-line">
      <h2 className="title-2">Tour Program</h2>
      <div className="pl-30 tb:pl-20 mbl:pl-0">
        <Warning className="mt-20 mb-30">
          The private tour can be changed or created depending on your
          preferences
        </Warning>
        <div>
          {data.program.map((program, key) => (
            <Accordeon
              key={key}
              title={
                <div className="flex items-center gap-[20px] mbl:gap-[5px]">
                  <span className="flex justify-center items-center w-[80px] h-[80px] flex-shrink-0 rounded-[50%] bg-blue font-medium text-white tb:w-[60px] tb:h-[60px] tb:text-[16px] tb:font-normal">
                    Day {program.day}
                  </span>
                  <h3 className=" text-[24px] text-start leading-[28px] font-normal tb:text-[20px] tb:leading-[23px] smbl:text-[18px]">
                    {program.name}
                  </h3>
                </div>
              }
              className="[&:not(:last-child)]:mb-30"
              marginTop={42}
            >
              {program.locations.map((location, key) => (
                <div key={key}>
                  <div className="relative flex items-center gap-[8px] leading-[18px] font-medium">
                    <img src={getIconLocation(location.type)} alt="route" />
                    <span>{location.name_location}</span>
                    <p className="absolute top-0 left-[180px] font-normal text-start">
                      {!isTb
                        ? location.description_location
                        : location.description_location
                            ?.split(".")
                            .slice(0, 3)
                            .join(".")}
                    </p>
                  </div>
                  {key + 1 < program.locations.length && (
                    <>
                      <img className="my-10 pl-[50px]" src={road} alt="road" />
                      <div className="relative flex items-center gap-[8px] leading-[18px]">
                        <img
                          src={getIconMoving(location.nextTransport.type)}
                          alt="route"
                        />
                        <span>{location.nextTransport.time}</span>
                      </div>
                      <img className="my-10 pl-[50px]" src={road} alt="road" />
                    </>
                  )}
                </div>
              ))}
            </Accordeon>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Program;
